"""
Tests for MaxoContracts Blocks (ConditionBlock, ActionBlock)
"""
import pytest
from decimal import Decimal
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from maxocontracts.core.types import VHV
from maxocontracts.blocks.condition import ConditionBlock, CommonConditions
from maxocontracts.blocks.action import ActionBlock, CommonActions

# --- ConditionBlock Tests ---

def test_condition_block_evaluation_success():
    """Test valid condition evaluation."""
    cond = ConditionBlock(
        condition_id="test_balance",
        description="Check balance > 10",
        predicate=lambda ctx: ctx.get("balance", 0) > 10,
        civil_language="Tienes suficiente saldo"
    )
    
    context = {"balance": 20}
    result = cond.evaluate(context)
    
    assert result.passed is True
    assert result.condition_id == "test_balance"
    assert result.context_snapshot == context

def test_condition_block_evaluation_failure():
    """Test failed condition evaluation."""
    cond = ConditionBlock(
        condition_id="test_balance_fail",
        description="Check balance > 10",
        predicate=lambda ctx: ctx.get("balance", 0) > 10
    )
    
    context = {"balance": 5}
    result = cond.evaluate(context)
    
    assert result.passed is False
    assert result.reason == "Condición no satisfecha"

def test_condition_block_exception_handling():
    """Test handling of exceptions within predicate."""
    cond = ConditionBlock(
        condition_id="test_error",
        description="Fails with error",
        predicate=lambda ctx: ctx["non_existent_key"] > 0
    )
    
    result = cond.evaluate({})
    assert result.passed is False
    assert "Error en evaluación" in result.reason
    assert "KeyError" in result.reason or "non_existent_key" in result.reason

def test_condition_civil_language_limit():
    """Test validation of civil language length."""
    long_text = "word " * 30
    with pytest.raises(ValueError) as excinfo:
        ConditionBlock(
            condition_id="fail", 
            description="desc", 
            predicate=lambda x: True, 
            civil_language=long_text
        )
    assert "civil excede límite" in str(excinfo.value)

def test_common_conditions():
    """Test factories for common conditions."""
    # Minimum Balance
    cond = CommonConditions.has_minimum_balance("wallet", 100)
    assert cond.evaluate({"wallet": 150}).passed is True
    assert cond.evaluate({"wallet": 50}).passed is False
    
    # Time Limit
    cond = CommonConditions.within_time_limit("deadline")
    # No deadline implies max time (always passes if current time is reasonably small, wait datetime.max is used)
    # Actually predicate matches if utcnow <= deadline. if deadline missing, it uses max, so passes.
    assert cond.evaluate({}).passed is True 

# --- ActionBlock Tests ---

def test_action_block_execution():
    """Test successful action execution."""
    cost = VHV(T=Decimal("1.0"), V=Decimal("0"), R=Decimal("0"))
    action = CommonActions.transfer_amount("user_a", "user_b", "amount", cost)
    
    ctx = {"user_a": 100, "user_b": 50, "amount": 20}
    result = action.execute(ctx)
    
    assert result.success is True
    assert result.context_after["user_a"] == 80
    assert result.context_after["user_b"] == 70
    assert result.vhv_consumed == cost
    assert len(action.get_execution_log()) == 1

def test_action_block_reversibility():
    """Test action retraction (reverse transformation)."""
    cost = VHV.zero()
    action = CommonActions.set_flag("active", True, cost)
    
    ctx = {"active": False}
    # Forward
    res_fwd = action.execute(ctx)
    assert res_fwd.success is True
    assert res_fwd.context_after["active"] is True
    
    # Reverse
    res_rev = action.reverse(res_fwd.context_after)
    assert res_rev.success is True
    assert res_rev.context_after["active"] is False
    assert res_rev.action_id.endswith("_REVERSE")
    # Retraction shouldn't consume VHV
    assert res_rev.vhv_consumed == VHV.zero()

def test_action_block_failure_safe():
    """Test action handles exceptions gracefully."""
    action = ActionBlock(
        action_id="fail_action",
        description="Fails",
        vhv_cost=VHV.zero(),
        transformer=lambda ctx: ctx["missing"] + 1
    )
    
    res = action.execute({})
    assert res.success is False
    assert res.context_after is None
    assert "KeyError" in res.error_message or "missing" in res.error_message

def test_action_missing_reverse():
    """Test error when reversing irreversible action."""
    action = ActionBlock(
        action_id="irreversible",
        description="Cant go back",
        vhv_cost=VHV.zero(),
        transformer=lambda ctx: ctx
    )
    
    assert action.is_reversible() is False
    with pytest.raises(ValueError) as excinfo:
        action.reverse({})
    assert "viola Invariante 4" in str(excinfo.value)
