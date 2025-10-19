# Documento de Diseño Técnico - Plataforma Común
## Versión Backend en Go + Bot de Telegram

**Versión:** 2.0 (Post-MVP)  
**Fecha:** Octubre 2025  
**Ingeniero Principal:** Max López
**Estado:** Diseño para implementación futura

---

## 1. Visión General

### 1.1 Contexto
Después de validar el concepto de Maxocracia con el MVP manual (Google Forms + Sheets), construimos una plataforma escalable que soporte:
- Miles de usuarios concurrentes
- Matching automático inteligente
- Sistema de puntos Maxo robusto
- Múltiples interfaces (Telegram Bot, Web App futura, Discord Bot)

### 1.2 Principios de Diseño
- **Simplicidad primero**: Resolver problemas reales, no agregar features innecesarias
- **Escalabilidad horizontal**: Preparado para crecer sin reescribir
- **Observabilidad**: Saber qué pasa en producción en todo momento
- **Resiliencia**: Fallos aislados no tumban el sistema completo
- **Ética by design**: Privacidad y transparencia incorporadas

---

## 2. Arquitectura del Sistema

### 2.1 Vista de Alto Nivel

```
┌─────────────────┐
│  Telegram Bot   │
│   (Interfaz)    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│       API Gateway (Go)              │
│  - Rate limiting                    │
│  - Authentication                   │
│  - Request routing                  │
└────────┬────────────────────────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
┌────────┐ ┌──────┐ ┌────────┐ ┌───────┐
│ User   │ │Match │ │ Maxo   │ │Social │
│Service │ │Engine│ │Service │ │Service│
└───┬────┘ └──┬───┘ └───┬────┘ └───┬───┘
    │         │          │          │
    └─────────┴──────────┴──────────┘
                   │
            ┌──────┴──────┐
            ▼             ▼
      ┌──────────┐   ┌────────┐
      │ MongoDB  │   │ Redis  │
      │ (Primary)│   │(Cache) │
      └──────────┘   └────────┘
```

### 2.2 Decisiones Arquitectónicas

#### ¿Por qué Go?
- ✅ Compilación rápida (importante en tu hardware)
- ✅ Goroutines nativas para concurrencia
- ✅ Tipado estático (menos bugs en producción)
- ✅ Deploy simple (un binario)
- ✅ Excelente para APIs y microservicios

#### ¿Por qué MongoDB?
- ✅ Esquema flexible (Maxocracia evolucionará)
- ✅ Queries rápidas por geolocalización
- ✅ Escala horizontal fácilmente
- ✅ Atlas (managed) reduce ops

#### ¿Por qué Redis?
- ✅ Cache de sesiones de usuario
- ✅ Rate limiting distribuido
- ✅ Pub/Sub para notificaciones en tiempo real
- ✅ Reduce carga en MongoDB

---

## 3. Microservicios Detallados

### 3.1 User Service

**Responsabilidad:** Gestión de usuarios, autenticación, perfiles

#### Endpoints:
```
POST   /api/v1/users/register
POST   /api/v1/users/login
GET    /api/v1/users/:id
PATCH  /api/v1/users/:id
GET    /api/v1/users/:id/stats
DELETE /api/v1/users/:id
```

#### Modelo de Datos (MongoDB):
```go
type User struct {
    ID            primitive.ObjectID `bson:"_id,omitempty"`
    TelegramID    int64              `bson:"telegram_id" json:"telegram_id"`
    Username      string             `bson:"username" json:"username"`
    FullName      string             `bson:"full_name" json:"full_name"`
    Email         string             `bson:"email,omitempty" json:"email,omitempty"`
    Phone         string             `bson:"phone,omitempty" json:"phone,omitempty"`
    
    Location      Location           `bson:"location" json:"location"`
    Skills        []string           `bson:"skills" json:"skills"`
    Interests     []string           `bson:"interests" json:"interests"`
    
    MaxoBalance   int                `bson:"maxo_balance" json:"maxo_balance"`
    Reputation    float64            `bson:"reputation" json:"reputation"`
    
    Stats         UserStats          `bson:"stats" json:"stats"`
    
    CreatedAt     time.Time          `bson:"created_at" json:"created_at"`
    UpdatedAt     time.Time          `bson:"updated_at" json:"updated_at"`
    LastActiveAt  time.Time          `bson:"last_active_at" json:"last_active_at"`
}

type Location struct {
    City          string             `bson:"city" json:"city"`
    Neighborhood  string             `bson:"neighborhood,omitempty" json:"neighborhood,omitempty"`
    Coordinates   GeoJSON            `bson:"coordinates" json:"coordinates"`
}

type GeoJSON struct {
    Type          string             `bson:"type" json:"type"`
    Coordinates   [2]float64         `bson:"coordinates" json:"coordinates"` // [lng, lat]
}

type UserStats struct {
    NeedsPosted      int    `bson:"needs_posted" json:"needs_posted"`
    ResourcesOffered int    `bson:"resources_offered" json:"resources_offered"`
    MatchesCompleted int    `bson:"matches_completed" json:"matches_completed"`
    MaxosEarned      int    `bson:"maxos_earned" json:"maxos_earned"`
    MaxosSpent       int    `bson:"maxos_spent" json:"maxos_spent"`
}
```

#### Lógica de Negocio:
- **Registro**: Validar Telegram ID único, crear wallet de Maxo inicial (50 puntos)
- **Autenticación**: JWT tokens con refresh token en Redis
- **Perfiles**: Actualización incremental, validación de datos
- **Geolocalización**: Índice 2dsphere en MongoDB para búsquedas por proximidad

---

### 3.2 Resource Service

**Responsabilidad:** Gestión de necesidades y recursos publicados

#### Endpoints:
```
POST   /api/v1/resources
GET    /api/v1/resources
GET    /api/v1/resources/:id
PATCH  /api/v1/resources/:id
DELETE /api/v1/resources/:id
GET    /api/v1/resources/search
GET    /api/v1/resources/nearby
```

#### Modelo de Datos:
```go
type Resource struct {
    ID           primitive.ObjectID `bson:"_id,omitempty"`
    UserID       primitive.ObjectID `bson:"user_id" json:"user_id"`
    
    Type         ResourceType       `bson:"type" json:"type"` // need | offer
    Category     Category           `bson:"category" json:"category"`
    
    Title        string             `bson:"title" json:"title"`
    Description  string             `bson:"description" json:"description"`
    Tags         []string           `bson:"tags" json:"tags"`
    
    Location     Location           `bson:"location" json:"location"`
    
    Urgency      UrgencyLevel       `bson:"urgency" json:"urgency"`
    Status       ResourceStatus     `bson:"status" json:"status"`
    
    Images       []string           `bson:"images,omitempty" json:"images,omitempty"`
    
    Conditions   string             `bson:"conditions,omitempty" json:"conditions,omitempty"`
    
    ViewCount    int                `bson:"view_count" json:"view_count"`
    MatchCount   int                `bson:"match_count" json:"match_count"`
    
    CreatedAt    time.Time          `bson:"created_at" json:"created_at"`
    UpdatedAt    time.Time          `bson:"updated_at" json:"updated_at"`
    ExpiresAt    *time.Time         `bson:"expires_at,omitempty" json:"expires_at,omitempty"`
}

type ResourceType string
const (
    TypeNeed  ResourceType = "need"
    TypeOffer ResourceType = "offer"
)

type Category string
const (
    CategoryObject     Category = "object"
    CategorySkill      Category = "skill"
    CategoryKnowledge  Category = "knowledge"
    CategoryMoney      Category = "money"
    CategorySpace      Category = "space"
    CategoryTransport  Category = "transport"
    CategoryTime       Category = "time"
    CategoryOther      Category = "other"
)

type UrgencyLevel string
const (
    UrgencyHigh   UrgencyLevel = "high"
    UrgencyMedium UrgencyLevel = "medium"
    UrgencyLow    UrgencyLevel = "low"
)

type ResourceStatus string
const (
    StatusActive    ResourceStatus = "active"
    StatusMatched   ResourceStatus = "matched"
    StatusCompleted ResourceStatus = "completed"
    StatusExpired   ResourceStatus = "expired"
    StatusCancelled ResourceStatus = "cancelled"
)
```

#### Índices MongoDB:
```javascript
// Búsqueda geoespacial
db.resources.createIndex({ "location.coordinates": "2dsphere" })

// Búsqueda por categoría y tipo
db.resources.createIndex({ "category": 1, "type": 1, "status": 1 })

// Búsqueda por usuario
db.resources.createIndex({ "user_id": 1, "created_at": -1 })

// Búsqueda de texto completo
db.resources.createIndex({ 
    "title": "text", 
    "description": "text", 
    "tags": "text" 
})

// TTL para expiración automática
db.resources.createIndex({ "expires_at": 1 }, { expireAfterSeconds: 0 })
```

---

### 3.3 Match Engine

**Responsabilidad:** Encontrar coincidencias entre necesidades y recursos

#### Endpoints:
```
POST   /api/v1/matches/find        # Buscar matches para un recurso
GET    /api/v1/matches/:id
POST   /api/v1/matches/:id/accept
POST   /api/v1/matches/:id/reject
POST   /api/v1/matches/:id/complete
GET    /api/v1/matches/user/:userId
```

#### Modelo de Datos:
```go
type Match struct {
    ID              primitive.ObjectID `bson:"_id,omitempty"`
    
    NeedID          primitive.ObjectID `bson:"need_id" json:"need_id"`
    OfferID         primitive.ObjectID `bson:"offer_id" json:"offer_id"`
    
    RequesterID     primitive.ObjectID `bson:"requester_id" json:"requester_id"`
    ProviderID      primitive.ObjectID `bson:"provider_id" json:"provider_id"`
    
    Score           float64            `bson:"score" json:"score"` // 0-100
    MatchReasons    []string           `bson:"match_reasons" json:"match_reasons"`
    
    Status          MatchStatus        `bson:"status" json:"status"`
    
    AcceptedBy      []primitive.ObjectID `bson:"accepted_by" json:"accepted_by"`
    RejectedBy      []primitive.ObjectID `bson:"rejected_by" json:"rejected_by"`
    
    CompletedAt     *time.Time         `bson:"completed_at,omitempty" json:"completed_at,omitempty"`
    
    MaxoTransaction primitive.ObjectID `bson:"maxo_transaction,omitempty" json:"maxo_transaction,omitempty"`
    
    CreatedAt       time.Time          `bson:"created_at" json:"created_at"`
    UpdatedAt       time.Time          `bson:"updated_at" json:"updated_at"`
}

type MatchStatus string
const (
    MatchPending   MatchStatus = "pending"
    MatchAccepted  MatchStatus = "accepted"
    MatchRejected  MatchStatus = "rejected"
    MatchCompleted MatchStatus = "completed"
    MatchExpired   MatchStatus = "expired"
)
```

#### Algoritmo de Matching:

```go
func (e *MatchEngine) FindMatches(ctx context.Context, resourceID primitive.ObjectID) ([]Match, error) {
    // 1. Obtener el recurso base
    resource, err := e.resourceRepo.GetByID(ctx, resourceID)
    if err != nil {
        return nil, err
    }
    
    // 2. Determinar el tipo opuesto
    oppositeType := TypeOffer
    if resource.Type == TypeOffer {
        oppositeType = TypeNeed
    }
    
    // 3. Construir query de búsqueda
    filter := bson.M{
        "type":     oppositeType,
        "category": resource.Category,
        "status":   StatusActive,
    }
    
    // 4. Búsqueda por proximidad geográfica (radio 50km)
    if resource.Location.Coordinates.Coordinates[0] != 0 {
        filter["location.coordinates"] = bson.M{
            "$near": bson.M{
                "$geometry": bson.M{
                    "type":        "Point",
                    "coordinates": resource.Location.Coordinates.Coordinates,
                },
                "$maxDistance": 50000, // 50km en metros
            },
        }
    }
    
    candidates, err := e.resourceRepo.Find(ctx, filter)
    if err != nil {
        return nil, err
    }
    
    // 5. Calcular score de cada candidato
    matches := []Match{}
    for _, candidate := range candidates {
        score := e.calculateMatchScore(resource, candidate)
        
        if score >= 30.0 { // Umbral mínimo de matching
            match := Match{
                NeedID:       getNeedID(resource, candidate),
                OfferID:      getOfferID(resource, candidate),
                RequesterID:  getRequesterID(resource, candidate),
                ProviderID:   getProviderID(resource, candidate),
                Score:        score,
                MatchReasons: e.getMatchReasons(resource, candidate, score),
                Status:       MatchPending,
                CreatedAt:    time.Now(),
                UpdatedAt:    time.Now(),
            }
            matches = append(matches, match)
        }
    }
    
    // 6. Ordenar por score descendente
    sort.Slice(matches, func(i, j int) bool {
        return matches[i].Score > matches[j].Score
    })
    
    // 7. Limitar a top 10
    if len(matches) > 10 {
        matches = matches[:10]
    }
    
    return matches, nil
}

func (e *MatchEngine) calculateMatchScore(r1, r2 Resource) float64 {
    score := 0.0
    
    // Categoría exacta: 30 puntos
    if r1.Category == r2.Category {
        score += 30.0
    }
    
    // Similitud de texto (title + description): 0-25 puntos
    textScore := e.calculateTextSimilarity(
        r1.Title+" "+r1.Description,
        r2.Title+" "+r2.Description,
    )
    score += textScore * 25.0
    
    // Tags compartidos: 0-15 puntos
    tagScore := e.calculateTagOverlap(r1.Tags, r2.Tags)
    score += tagScore * 15.0
    
    // Proximidad geográfica: 0-20 puntos
    distance := e.calculateDistance(r1.Location, r2.Location)
    if distance < 5 {      // < 5km
        score += 20.0
    } else if distance < 15 {  // 5-15km
        score += 15.0
    } else if distance < 30 {  // 15-30km
        score += 10.0
    } else if distance < 50 {  // 30-50km
        score += 5.0
    }
    
    // Urgencia: 0-10 puntos bonus
    if (r1.Urgency == UrgencyHigh || r2.Urgency == UrgencyHigh) {
        score += 10.0
    }
    
    return score
}
```

---

### 3.4 Maxo Service

**Responsabilidad:** Sistema de puntos, transacciones, economía

#### Endpoints:
```
GET    /api/v1/maxo/balance/:userId
POST   /api/v1/maxo/transfer
GET    /api/v1/maxo/transactions/:userId
GET    /api/v1/maxo/leaderboard
POST   /api/v1/maxo/calculate-reward
```

#### Modelo de Datos:
```go
type MaxoTransaction struct {
    ID          primitive.ObjectID `bson:"_id,omitempty"`
    
    FromUserID  *primitive.ObjectID `bson:"from_user_id,omitempty" json:"from_user_id,omitempty"`
    ToUserID    primitive.ObjectID  `bson:"to_user_id" json:"to_user_id"`
    
    Amount      int                 `bson:"amount" json:"amount"`
    Type        TransactionType     `bson:"type" json:"type"`
    Reason      string              `bson:"reason" json:"reason"`
    
    MatchID     *primitive.ObjectID `bson:"match_id,omitempty" json:"match_id,omitempty"`
    ResourceID  *primitive.ObjectID `bson:"resource_id,omitempty" json:"resource_id,omitempty"`
    
    Metadata    map[string]interface{} `bson:"metadata,omitempty" json:"metadata,omitempty"`
    
    CreatedAt   time.Time           `bson:"created_at" json:"created_at"`
}

type TransactionType string
const (
    TxWelcomeBonus      TransactionType = "welcome_bonus"
    TxPostResource      TransactionType = "post_resource"
    TxMatchCompleted    TransactionType = "match_completed"
    TxRatingReceived    TransactionType = "rating_received"
    TxDailyActive       TransactionType = "daily_active"
    TxReferralBonus     TransactionType = "referral_bonus"
    TxCommunityVote     TransactionType = "community_vote"
    TxTransfer          TransactionType = "transfer"
)
```

#### Sistema de Recompensas:
```go
var RewardTable = map[TransactionType]int{
    TxWelcomeBonus:   50,   // Al registrarse
    TxPostResource:   5,    // Por publicar necesidad/recurso
    TxMatchCompleted: 20,   // Por completar un match
    TxRatingReceived: 3,    // Por recibir calificación positiva
    TxDailyActive:    2,    // Por actividad diaria
    TxReferralBonus:  15,   // Por invitar a alguien que se une
    TxCommunityVote:  1,    // Por participar en votaciones
}

// Bonificación por impacto
func CalculateImpactBonus(match Match) int {
    baseReward := RewardTable[TxMatchCompleted]
    
    // Multiplicador por urgencia
    urgencyMultiplier := 1.0
    if match.Urgency == UrgencyHigh {
        urgencyMultiplier = 1.5
    }
    
    // Multiplicador por categoría
    categoryMultiplier := 1.0
    switch match.Category {
    case CategoryMoney, CategorySpace:
        categoryMultiplier = 1.3 // Mayor impacto social
    }
    
    // Multiplicador por calificación
    ratingMultiplier := match.Rating / 5.0
    
    total := float64(baseReward) * urgencyMultiplier * categoryMultiplier * ratingMultiplier
    
    return int(math.Round(total))
}
```

#### Lógica de Transferencia:
```go
func (s *MaxoService) Transfer(ctx context.Context, tx MaxoTransaction) error {
    // 1. Iniciar sesión MongoDB (transacción ACID)
    session, err := s.client.StartSession()
    if err != nil {
        return err
    }
    defer session.EndSession(ctx)
    
    err = mongo.WithSession(ctx, session, func(sc mongo.SessionContext) error {
        // 2. Verificar balance (si hay fromUser)
        if tx.FromUserID != nil {
            fromUser, err := s.userRepo.GetByID(sc, *tx.FromUserID)
            if err != nil {
                return err
            }
            if fromUser.MaxoBalance < tx.Amount {
                return ErrInsufficientBalance
            }
            
            // 3. Restar del origen
            err = s.userRepo.UpdateBalance(sc, *tx.FromUserID, -tx.Amount)
            if err != nil {
                return err
            }
        }
        
        // 4. Sumar al destino
        err = s.userRepo.UpdateBalance(sc, tx.ToUserID, tx.Amount)
        if err != nil {
            return err
        }
        
        // 5. Registrar transacción
        tx.CreatedAt = time.Now()
        _, err = s.txRepo.Create(sc, tx)
        if err != nil {
            return err
        }
        
        // 6. Notificar via Redis pub/sub
        s.notifyBalanceChange(sc, tx.ToUserID, tx.Amount)
        
        return nil
    })
    
    return err
}
```

---

### 3.5 Social Service

**Responsabilidad:** Interacciones, calificaciones, mensajes

#### Endpoints:
```
POST   /api/v1/social/rate
GET    /api/v1/social/ratings/:userId
POST   /api/v1/social/report
GET    /api/v1/social/conversations/:userId
```

#### Modelo de Datos:
```go
type Rating struct {
    ID          primitive.ObjectID `bson:"_id,omitempty"`
    
    FromUserID  primitive.ObjectID `bson:"from_user_id" json:"from_user_id"`
    ToUserID    primitive.ObjectID `bson:"to_user_id" json:"to_user_id"`
    MatchID     primitive.ObjectID `bson:"match_id" json:"match_id"`
    
    Score       int                `bson:"score" json:"score"` // 1-5
    Comment     string             `bson:"comment,omitempty" json:"comment,omitempty"`
    
    Categories  RatingCategories   `bson:"categories" json:"categories"`
    
    CreatedAt   time.Time          `bson:"created_at" json:"created_at"`
}

type RatingCategories struct {
    Communication   int `bson:"communication" json:"communication"` // 1-5
    Punctuality     int `bson:"punctuality" json:"punctuality"`
    Quality         int `bson:"quality" json:"quality"`
    Friendliness    int `bson:"friendliness" json:"friendliness"`
}
```

---

## 4. Telegram Bot

### 4.1 Arquitectura del Bot

```go
package bot

type Bot struct {
    api        *tgbotapi.BotAPI
    apiClient  *APIClient      // Cliente HTTP al backend
    redis      *redis.Client
    logger     *zap.Logger
}

func (b *Bot) Start() error {
    u := tgbotapi.NewUpdate(0)
    u.Timeout = 60
    
    updates := b.api.GetUpdatesChan(u)
    
    for update := range updates {
        go b.handleUpdate(update) // Goroutine por update
    }
    
    return nil
}
```

### 4.2 Comandos Principales

```go
var Commands = []tgbotapi.BotCommand{
    {Command: "start", Description: "Iniciar y registrarse"},
    {Command: "ayuda", Description: "Ver comandos disponibles"},
    
    {Command: "necesito", Description: "Publicar una necesidad"},
    {Command: "ofrezco", Description: "Publicar un recurso"},
    {Command: "buscar", Description: "Buscar recursos o necesidades"},
    
    {Command: "mispublicaciones", Description: "Ver mis publicaciones"},
    {Command: "mismatches", Description: "Ver mis coincidencias"},
    
    {Command: "maxo", Description: "Ver mi balance de Maxos"},
    {Command: "perfil", Description: "Ver/editar mi perfil"},
    {Command: "stats", Description: "Ver mis estadísticas"},
    
    {Command: "ranking", Description: "Ver ranking de colaboradores"},
    {Command: "sobre", Description: "Sobre la Maxocracia"},
}
```

### 4.3 Flujos Conversacionales

#### Flujo: Publicar Necesidad
```
Usuario: /necesito

Bot: 🎯 ¿Qué necesitas?
     Selecciona una categoría:
     
     [📦 Objeto]  [🛠️ Habilidad]
     [📚 Conocimiento]  [💰 Apoyo económico]
     [🏠 Espacio]  [🚗 Transporte]
     [⏰ Tiempo]  [🌱 Otro]

Usuario: [presiona "Objeto"]

Bot: 📦 Objeto seleccionado.
     
     Describe qué objeto necesitas:
     Ejemplo: "Bicicleta en buen estado para ir al trabajo"

Usuario: "Mesa de estudio pequeña"

Bot: ✅ Entendido: "Mesa de estudio pequeña"
     
     📍 ¿Dónde te encuentras?
     
     [📍 Compartir ubicación]
     [✍️ Escribir ciudad/barrio]

Usuario: [comparte ubicación]

Bot: 📍 Ubicación: Bogotá, Chapinero
     
     ⏱️ ¿Qué tan urgente es?
     
     [🔴 Muy urgente]
     [🟡 Moderado]
     [🟢 No urgente]

Usuario: [presiona "Moderado"]

Bot: ✅ ¡Necesidad publicada!
     
     📋 Resumen:
     • Categoría: Objeto
     • Necesitas: Mesa de estudio pequeña
     • Ubicación: Bogotá, Chapinero
     • Urgencia: Moderada
     
     🔍 Buscando coincidencias...
     Te notificaré si encuentro algo.
     
     🎉 Has ganado +5 Maxos
     Tu balance: 55 Maxos
     
     [Ver mis publicaciones] [Publicar otra]
```

### 4.4 Estados Conversacionales con Redis

```go
type ConversationState struct {
    UserID      int64
    CurrentFlow string
    Step        int
    Data        map[string]interface{}
    ExpiresAt   time.Time
}

// Guardar estado en Redis
func (b *Bot) SaveState(state ConversationState) error {
    key := fmt.Sprintf("conv:%d", state.UserID)
    data, _ := json.Marshal(state)
    return b.redis.Set(context.Background(), key, data, 10*time.Minute).Err()
}

// Recuperar estado
func (b *Bot) GetState(userID int64) (*ConversationState, error) {
    key := fmt.Sprintf("conv:%d", userID)
    data, err := b.redis.Get(context.Background(), key).Result()
    if err != nil {
        return nil, err
    }
    
    var state ConversationState
    json.Unmarshal([]byte(data), &state)
    return &state, nil
}
```

---

## 5. Infraestructura y Deployment

### 5.1 Stack de Infraestructura

```yaml
# docker-compose.yml
version: '3.8'

services:
  # API Gateway
  gateway:
    build: ./services/gateway
    ports:
      - "8080:8080"
    environment:
      - MONGO_URI=${MONGO_URI}
      - REDIS_URI=${REDIS_URI}
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      - redis
  
  # User Service
  user-service:
    build: ./services/user
    environment:
      - MONGO_URI=${MONGO_URI}
      - REDIS_URI=${REDIS_URI}
    depends_on:
      - redis
  
  # Resource Service
  resource-service:
    build: ./services/resource
    environment:
      - MONGO_URI=${MONGO_URI}
  
  # Match Engine
  match-engine:
    build: ./services/match
    environment:
      - MONGO_URI=${MONGO_URI}
      - REDIS_URI=${REDIS_URI}
  
  # Maxo Service
  maxo-service:
    build: ./services/maxo
    environment:
      - MONGO_URI=${MONGO_URI}
  
  # Telegram Bot
  telegram-bot:
    build: ./services/bot
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - API_GATEWAY_URL=http://gateway:8080
      - REDIS_URI=${REDIS_URI}
    depends_on:
      - gateway
      - redis
  
  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

### 5.2 Estructura de Proyecto

```
comun/
├── cmd/
│   ├── gateway/
│   │   └── main.go
│   ├── user-service/
│   │   └── main.go
│   ├── resource-service/
│   │   └── main.go
│   ├── match-engine/
│   │   └── main.go
│   ├── maxo-service/
│   │   └── main.go
│   ├── social-service/
│   │   └── main.go
│   └── telegram-bot/
│       └── main.go
├── internal/
│   ├── domain/           # Modelos de dominio
│   │   ├── user.go
│   │   ├── resource.go
│   │   ├── match.go
│   │   └── maxo.go
│   ├── repository/       # Capa de acceso a datos
│   │   ├── user_repo.go
│   │   ├── resource_repo.go
│   │   └── match_repo.go
│   ├── service/          # Lógica de negocio
│   │   ├── user_service.go
│   │   ├── match_service.go
│   │   └── maxo_service.go
│   ├── handler/          # HTTP handlers
│   │   ├── user_handler.go
│   │   └── resource_handler.go
│   ├── middleware/       # Middlewares
│   │   ├── auth.go
│   │   ├── ratelimit.go
│   │   └── logging.go
│   └── bot/              # Lógica del bot
│       ├── handlers.go
│       ├── commands.go
│       └── keyboards.go
├── pkg/                  # Código compartido
│   ├── config/
│   │   └── config.go
│   ├── database/
│   │   ├── mongo.go
│   │   └── redis.go
│   ├── logger/
│   │   └── logger.go
│   └── utils/
│       ├── validation.go
│       └── geo.go
├── api/                  # OpenAPI specs
│   └── openapi.yaml
├── scripts/
│   ├── migrate.go
│   └── seed.go
├── docker-compose.yml
├── Makefile
├── go.mod
└── go.sum
```

### 5.3 Makefile para Desarrollo

```makefile
.PHONY: help build run test clean docker-up docker-down migrate

help: ## Mostrar ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $1, $2}'

build: ## Compilar todos los servicios
	@echo "🔨 Compilando servicios..."
	go build -o bin/gateway ./cmd/gateway
	go build -o bin/user-service ./cmd/user-service
	go build -o bin/resource-service ./cmd/resource-service
	go build -o bin/match-engine ./cmd/match-engine
	go build -o bin/maxo-service ./cmd/maxo-service
	go build -o bin/telegram-bot ./cmd/telegram-bot

run-gateway: ## Ejecutar API Gateway
	go run ./cmd/gateway/main.go

run-bot: ## Ejecutar Telegram Bot
	go run ./cmd/telegram-bot/main.go

test: ## Ejecutar tests
	go test -v -cover ./...

test-integration: ## Tests de integración
	go test -v -tags=integration ./...

lint: ## Linter
	golangci-lint run

docker-up: ## Levantar stack completo
	docker-compose up -d

docker-down: ## Detener stack
	docker-compose down

docker-logs: ## Ver logs
	docker-compose logs -f

migrate: ## Ejecutar migraciones
	go run ./scripts/migrate.go

seed: ## Poblar datos de prueba
	go run ./scripts/seed.go

clean: ## Limpiar binarios
	rm -rf bin/
```

---

## 6. Seguridad

### 6.1 Autenticación y Autorización

```go
// JWT con Telegram ID
type Claims struct {
    UserID     string `json:"user_id"`
    TelegramID int64  `json:"telegram_id"`
    Role       string `json:"role"`
    jwt.StandardClaims
}

func GenerateToken(user User) (string, error) {
    expirationTime := time.Now().Add(24 * time.Hour)
    
    claims := &Claims{
        UserID:     user.ID.Hex(),
        TelegramID: user.TelegramID,
        Role:       "user",
        StandardClaims: jwt.StandardClaims{
            ExpiresAt: expirationTime.Unix(),
            IssuedAt:  time.Now().Unix(),
        },
    }
    
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    return token.SignedString([]byte(os.Getenv("JWT_SECRET")))
}

// Middleware de autenticación
func AuthMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        authHeader := c.GetHeader("Authorization")
        if authHeader == "" {
            c.JSON(401, gin.H{"error": "token no proporcionado"})
            c.Abort()
            return
        }
        
        tokenString := strings.TrimPrefix(authHeader, "Bearer ")
        
        claims := &Claims{}
        token, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (interface{}, error) {
            return []byte(os.Getenv("JWT_SECRET")), nil
        })
        
        if err != nil || !token.Valid {
            c.JSON(401, gin.H{"error": "token inválido"})
            c.Abort()
            return
        }
        
        // Inyectar claims en contexto
        c.Set("user_id", claims.UserID)
        c.Set("telegram_id", claims.TelegramID)
        c.Next()
    }
}
```

### 6.2 Rate Limiting

```go
// Rate limiter con Redis
type RateLimiter struct {
    redis *redis.Client
}

func (rl *RateLimiter) Allow(ctx context.Context, key string, limit int, window time.Duration) (bool, error) {
    pipe := rl.redis.Pipeline()
    
    // Incrementar contador
    incrCmd := pipe.Incr(ctx, key)
    
    // Establecer expiración si es nueva key
    pipe.Expire(ctx, key, window)
    
    _, err := pipe.Exec(ctx)
    if err != nil {
        return false, err
    }
    
    count := incrCmd.Val()
    return count <= int64(limit), nil
}

// Middleware de rate limiting
func RateLimitMiddleware(limiter *RateLimiter) gin.HandlerFunc {
    return func(c *gin.Context) {
        userID := c.GetString("user_id")
        if userID == "" {
            userID = c.ClientIP()
        }
        
        key := fmt.Sprintf("ratelimit:%s", userID)
        
        allowed, err := limiter.Allow(c.Request.Context(), key, 100, time.Minute)
        if err != nil {
            c.JSON(500, gin.H{"error": "error de rate limiting"})
            c.Abort()
            return
        }
        
        if !allowed {
            c.JSON(429, gin.H{"error": "demasiadas solicitudes"})
            c.Abort()
            return
        }
        
        c.Next()
    }
}
```

### 6.3 Validación de Datos

```go
// Usar validator
type CreateResourceRequest struct {
    Type        string   `json:"type" binding:"required,oneof=need offer"`
    Category    string   `json:"category" binding:"required"`
    Title       string   `json:"title" binding:"required,min=5,max=100"`
    Description string   `json:"description" binding:"required,min=10,max=1000"`
    Tags        []string `json:"tags" binding:"max=10,dive,max=30"`
    City        string   `json:"city" binding:"required"`
    Urgency     string   `json:"urgency" binding:"required,oneof=high medium low"`
}

// Handler con validación
func (h *ResourceHandler) Create(c *gin.Context) {
    var req CreateResourceRequest
    
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(400, gin.H{"error": "datos inválidos", "details": err.Error()})
        return
    }
    
    // Sanitizar inputs
    req.Title = html.EscapeString(req.Title)
    req.Description = html.EscapeString(req.Description)
    
    // Continuar con lógica...
}
```

---

## 7. Observabilidad

### 7.1 Logging Estructurado

```go
// Usar zap para logging
import "go.uber.org/zap"

var logger *zap.Logger

func InitLogger() {
    var err error
    if os.Getenv("ENVIRONMENT") == "production" {
        logger, err = zap.NewProduction()
    } else {
        logger, err = zap.NewDevelopment()
    }
    
    if err != nil {
        panic(err)
    }
}

// Uso en handlers
func (h *ResourceHandler) Create(c *gin.Context) {
    logger.Info("creating resource",
        zap.String("user_id", c.GetString("user_id")),
        zap.String("category", req.Category),
    )
    
    // ...
    
    logger.Info("resource created",
        zap.String("resource_id", resource.ID.Hex()),
        zap.Duration("duration", time.Since(start)),
    )
}
```

### 7.2 Métricas

```go
// Prometheus metrics
import (
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
)

var (
    resourcesCreated = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "comun_resources_created_total",
            Help: "Total de recursos creados",
        },
        []string{"type", "category"},
    )
    
    matchesFound = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name: "comun_matches_found",
            Help: "Número de matches encontrados",
            Buckets: []float64{0, 1, 3, 5, 10, 20},
        },
        []string{"category"},
    )
    
    apiLatency = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name: "comun_api_latency_seconds",
            Help: "Latencia de API",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "endpoint", "status"},
    )
)

// Middleware de métricas
func MetricsMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        
        c.Next()
        
        duration := time.Since(start).Seconds()
        status := fmt.Sprintf("%d", c.Writer.Status())
        
        apiLatency.WithLabelValues(
            c.Request.Method,
            c.FullPath(),
            status,
        ).Observe(duration)
    }
}
```

### 7.3 Health Checks

```go
type HealthChecker struct {
    mongo *mongo.Client
    redis *redis.Client
}

func (h *HealthChecker) Check(c *gin.Context) {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    
    health := gin.H{
        "status": "healthy",
        "timestamp": time.Now().Unix(),
    }
    
    // Check MongoDB
    if err := h.mongo.Ping(ctx, nil); err != nil {
        health["status"] = "unhealthy"
        health["mongodb"] = "down"
        c.JSON(503, health)
        return
    }
    health["mongodb"] = "up"
    
    // Check Redis
    if err := h.redis.Ping(ctx).Err(); err != nil {
        health["status"] = "unhealthy"
        health["redis"] = "down"
        c.JSON(503, health)
        return
    }
    health["redis"] = "up"
    
    c.JSON(200, health)
}
```

---

## 8. Testing

### 8.1 Estructura de Tests

```go
// internal/service/match_service_test.go
package service

import (
    "context"
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

// Mock del repositorio
type MockResourceRepo struct {
    mock.Mock
}

func (m *MockResourceRepo) Find(ctx context.Context, filter interface{}) ([]Resource, error) {
    args := m.Called(ctx, filter)
    return args.Get(0).([]Resource), args.Error(1)
}

// Test unitario
func TestFindMatches_WhenCandidatesExist_ReturnsMatches(t *testing.T) {
    // Arrange
    mockRepo := new(MockResourceRepo)
    engine := NewMatchEngine(mockRepo)
    
    need := Resource{
        Type:     TypeNeed,
        Category: CategoryObject,
        Title:    "Mesa de estudio",
    }
    
    offers := []Resource{
        {
            Type:     TypeOffer,
            Category: CategoryObject,
            Title:    "Mesa de madera",
        },
    }
    
    mockRepo.On("Find", mock.Anything, mock.Anything).Return(offers, nil)
    
    // Act
    matches, err := engine.FindMatches(context.Background(), need.ID)
    
    // Assert
    assert.NoError(t, err)
    assert.Len(t, matches, 1)
    assert.Greater(t, matches[0].Score, 0.0)
    mockRepo.AssertExpectations(t)
}
```

### 8.2 Tests de Integración

```go
// +build integration

package integration

import (
    "context"
    "testing"
    "github.com/testcontainers/testcontainers-go"
)

func TestMatchEngine_Integration(t *testing.T) {
    // Levantar MongoDB con testcontainers
    ctx := context.Background()
    
    mongoC, err := testcontainers.GenericContainer(ctx, testcontainers.GenericContainerRequest{
        ContainerRequest: testcontainers.ContainerRequest{
            Image:        "mongo:6",
            ExposedPorts: []string{"27017/tcp"},
        },
        Started: true,
    })
    if err != nil {
        t.Fatal(err)
    }
    defer mongoC.Terminate(ctx)
    
    // Obtener puerto
    port, _ := mongoC.MappedPort(ctx, "27017")
    uri := fmt.Sprintf("mongodb://localhost:%s", port.Port())
    
    // Conectar y probar
    client, _ := mongo.Connect(ctx, options.Client().ApplyURI(uri))
    defer client.Disconnect(ctx)
    
    // Test real contra MongoDB
    repo := NewResourceRepository(client)
    engine := NewMatchEngine(repo)
    
    // Crear recursos reales
    need := Resource{...}
    repo.Create(ctx, need)
    
    offer := Resource{...}
    repo.Create(ctx, offer)
    
    // Buscar matches
    matches, err := engine.FindMatches(ctx, need.ID)
    
    assert.NoError(t, err)
    assert.NotEmpty(t, matches)
}
```

---

## 9. Migración desde MVP

### 9.1 Plan de Migración de Datos

```go
// scripts/migrate.go
package main

import (
    "context"
    "encoding/csv"
    "os"
)

func MigrateFromSheets() error {
    // 1. Exportar Google Sheets a CSV
    // (manualmente o via API)
    
    // 2. Leer CSV
    file, err := os.Open("data_export.csv")
    if err != nil {
        return err
    }
    defer file.Close()
    
    reader := csv.NewReader(file)
    records, err := reader.ReadAll()
    if err != nil {
        return err
    }
    
    // 3. Conectar a MongoDB
    client, err := mongo.Connect(context.Background(), options.Client().ApplyURI(mongoURI))
    if err != nil {
        return err
    }
    defer client.Disconnect(context.Background())
    
    collection := client.Database("comun").Collection("resources")
    
    // 4. Transformar y insertar
    for i, record := range records {
        if i == 0 {
            continue // Skip header
        }
        
        resource := Resource{
            Type:        parseType(record[3]),
            Category:    parseCategory(record[4]),
            Title:       record[5],
            Description: record[6],
            Location: Location{
                City: record[7],
            },
            Urgency:   parseUrgency(record[9]),
            Status:    StatusActive,
            CreatedAt: parseDate(record[0]),
        }
        
        _, err := collection.InsertOne(context.Background(), resource)
        if err != nil {
            log.Printf("Error insertando recurso %d: %v", i, err)
            continue
        }
    }
    
    log.Println("Migración completada")
    return nil
}
```

### 9.2 Estrategia de Rollout

**Fase 1: Coexistencia (2 semanas)**
- MVP manual sigue funcionando
- Backend Go en staging
- 10-20 usuarios beta prueban el bot
- Datos se sincronizan manualmente

**Fase 2: Migración gradual (2-4 semanas)**
- Nuevos usuarios usan bot directamente
- Usuarios antiguos reciben invitación al bot
- Datos históricos se migran
- MVP manual solo para fallback

**Fase 3: Full production (semana 5+)**
- 100% en bot + backend Go
- MVP manual se depreca
- Monitoreo intensivo
- Iteración basada en feedback

---

## 10. Roadmap de Implementación

### 10.1 Sprint 1-2 (Setup inicial - 2 semanas)
- [ ] Configurar estructura de proyecto
- [ ] Setup MongoDB Atlas + Redis
- [ ] Modelos de dominio base
- [ ] Repository pattern
- [ ] API Gateway básico con Gin
- [ ] Docker compose local

### 10.2 Sprint 3-4 (User & Auth - 2 semanas)
- [ ] User Service completo
- [ ] Sistema de autenticación JWT
- [ ] Middleware de auth
- [ ] Endpoints de perfil
- [ ] Tests unitarios

### 10.3 Sprint 5-6 (Resources - 2 semanas)
- [ ] Resource Service
- [ ] CRUD de recursos
- [ ] Búsqueda y filtrado
- [ ] Geolocalización con MongoDB
- [ ] Tests

### 10.4 Sprint 7-8 (Match Engine - 2 semanas)
- [ ] Algoritmo de matching
- [ ] Scoring system
- [ ] Optimización de queries
- [ ] Cache con Redis
- [ ] Tests de matching

### 10.5 Sprint 9-10 (Maxo System - 2 semanas)
- [ ] Maxo Service
- [ ] Sistema de transacciones
- [ ] Cálculo de recompensas
- [ ] Leaderboard
- [ ] Tests transaccionales

### 10.6 Sprint 11-13 (Telegram Bot - 3 semanas)
- [ ] Bot básico (comandos)
- [ ] Flujos conversacionales
- [ ] Estados con Redis
- [ ] Keyboards inline
- [ ] Integración con backend
- [ ] Notificaciones

### 10.7 Sprint 14-15 (Social & Polish - 2 semanas)
- [ ] Sistema de calificaciones
- [ ] Reportes
- [ ] Dashboard web básico
- [ ] Documentación API
- [ ] Tests end-to-end

### 10.8 Sprint 16 (Deploy & Monitoring - 1 semana)
- [ ] Deploy a producción
- [ ] Setup monitoring (Prometheus + Grafana)
- [ ] Alertas
- [ ] Backup automatizado
- [ ] Migración de datos del MVP

**Total estimado: 16 semanas (~4 meses)**

---

## 11. Consideraciones de Producción

### 11.1 Escalabilidad

**Horizontal Scaling:**
```yaml
# Kubernetes deployment example (futuro)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: resource-service
spec:
  replicas: 3  # Múltiples instancias
  selector:
    matchLabels:
      app: resource-service
  template:
    metadata:
      labels:
        app: resource-service
    spec:
      containers:
      - name: resource-service
        image: comun/resource-service:latest
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
```

**Database Sharding (cuando sea necesario):**
- Shard key: `user_id` para recursos
- Replica sets para alta disponibilidad
- Read replicas para consultas pesadas

### 11.2 Backup y Disaster Recovery

```bash
# Script de backup automático
#!/bin/bash
# scripts/backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/mongodb"

# Backup de MongoDB
mongodump --uri="$MONGO_URI" --out="$BACKUP_DIR/$DATE"

# Comprimir
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" "$BACKUP_DIR/$DATE"
rm -rf "$BACKUP_DIR/$DATE"

# Subir a S3 (o storage de tu elección)
aws s3 cp "$BACKUP_DIR/backup_$DATE.tar.gz" s3://comun-backups/

# Mantener solo últimos 30 días
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +30 -delete

echo "Backup completado: $DATE"
```

### 11.3 Costos Estimados

**Infraestructura mínima (100-500 usuarios):**
- MongoDB Atlas (M10): $60/mes
- Redis Cloud (1GB): $12/mes
- VPS (2GB RAM): $10-20/mes
- **Total: ~$90/mes**

**Infraestructura media (1000-5000 usuarios):**
- MongoDB Atlas (M20): $150/mes
- Redis Cloud (5GB): $50/mes
- VPS x2 (4GB RAM): $40/mes
- CDN: $10/mes
- **Total: ~$250/mes**

---

## 12. Métricas de Éxito

### 12.1 KPIs Técnicos
- ✅ Latencia p95 < 200ms
- ✅ Uptime > 99.5%
- ✅ Error rate < 0.1%
- ✅ Match success rate > 60%

### 12.2 KPIs de Producto
- ✅ Usuarios activos mensuales
- ✅ Matches completados / Matches creados
- ✅ Tiempo promedio de resolución de necesidad
- ✅ NPS (Net Promoter Score)
- ✅ Tasa de retención semana 1 > 40%

---

## 13. Referencias y Recursos

### 13.1 Documentación
- [Go Documentation](https://go.dev/doc/)
- [MongoDB Go Driver](https://www.mongodb.com/docs/drivers/go/current/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Gin Web Framework](https://gin-gonic.com/docs/)

### 13.2 Librerías Clave
```go
// go.mod
module github.com/tuusuario/comun

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/go-telegram-bot-api/telegram-bot-api/v5 v5.5.1
    go.mongodb.org/mongo-driver v1.12.1
    github.com/redis/go-redis/v9 v9.2.1
    github.com/golang-jwt/jwt/v5 v5.0.0
    go.uber.org/zap v1.26.0
    github.com/prometheus/client_golang v1.17.0
)
```

---

## 14. Conclusión

Este diseño técnico proporciona una base sólida para construir la plataforma Común de manera escalable y mantenible. Las decisiones arquitectónicas están orientadas a:

1. **Simplicidad**: Empezar con lo necesario, crecer según demanda
2. **Pragmatismo**: Go + MongoDB + Redis son tecnologías probadas
3. **Ética**: Privacidad, transparencia y accesibilidad by design
4. **Resiliencia**: Fallos aislados, observabilidad completa
5. **Comunidad**: Código claro para que otros puedan contribuir

**Próximo paso:** Crear el repositorio, configurar el proyecto base, y comenzar con el Sprint 1.

---

*Documento vivo - se actualiza según aprendizajes durante implementación*

**Contacto técnico:** maxlopeztutor@gmail.com 
**Última actualización:** Octubre 2025