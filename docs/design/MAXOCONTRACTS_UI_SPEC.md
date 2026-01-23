# MaxoContracts UI Specification

## Overview
The "Contract Builder" is a visual interface allowing users to assemble MaxoContracts by combining "Term Blocks". It metaphorically represents a "legal LEGO set" where clarity and modularity are paramount.

## Design Philosophy
- **Aesthetic**: Premium Glassmorphism (consistent with `forms.css`).
- **Interaction**: Drag-and-Drop (Tactile, responsive).
- **Feedback**: Immediate validation visual cues (e.g., blocks snap together, invalid combinations glow red).

## Layout Structure

### 1. Left Sidebar (Navigation)
*Existing global navigation (Dashboard, etc.)*

### 2. Main Canvas (The Contract)
*Central drop zone.*
- **Header**: Contract Title, Participants, Total VHV Summary.
- **Body**: Infinite vertical scroll area where blocks are stacked.
- **Empty State**: "Drag term blocks here to start your contract."

### 3. Right Palette (The Toolkit)
*Tools panel.*
- **Categories**:
    - **Actions**: "Transfer Maxos", "Provide Service", "Deliver Good".
    - **Conditions**: "If...", "When...", "Until...".
    - **Participants**: "Add Giver", "Add Receiver".
- **Search**: Fast filter for blocks.

## Visual Components

### The "Term Block"
A rectangular card representing a single contract clause.
- **Background**: Translucent white (`rgba(255,255,255, 0.05)`).
- **Border**: Thin glass border (`1px solid rgba(255,255,255, 0.2)`).
- **Content**:
    - **Icon**: Represents type (e.g., ➡️ for transfer).
    - **Text**: "Alice pays 10 Maxos to Bob".
    - **VHV Tag**: Small badge showing VHV cost (T/V/R).
- **States**:
    - *Hover*: Slight lift + Glow.
    - *Dragging*: 50% opacity, follows cursor.
    - *Placed*: Solid, snaps to grid.

## Interactions
1.  **Drag**: Click and hold a block from the palette.
2.  **Drop Zone**: Valid drop areas on the canvas highlight (`rgba(52, 152, 219, 0.1)`).
3.  **Sort**: Reorder blocks by dragging up/down within the canvas.
4.  **Edit**: Click a placed block to open "Edit Modal" (modify values/participants).

## Color Palette extensions
- **Block Action**: `var(--color-maxo)` (Blue/Purple gradient).
- **Block Condition**: `var(--color-urgency-medium)` (Orange).
- **Block Validation**: `var(--color-forms-success)` (Green).
