# Datathon 2026 - Data Schema (ERD)

Sơ đồ quan hệ thực thể (ERD) mô tả cấu trúc liên kết giữa các bảng dữ liệu trong hệ thống:

```mermaid
erDiagram
    %% Master Data
    GEOGRAPHY ||--o{ CUSTOMERS : "zip"
    GEOGRAPHY ||--o{ ORDERS : "zip"
    CUSTOMERS ||--o{ ORDERS : "customer_id"
    PRODUCTS ||--o{ ORDER_ITEMS : "product_id"
    PRODUCTS ||--o{ INVENTORY : "product_id"
    PROMOTIONS ||--o{ ORDER_ITEMS : "promo_id"

    %% Transaction Data
    ORDERS ||--o{ ORDER_ITEMS : "order_id"
    ORDERS ||--|| PAYMENTS : "order_id (1:1)"
    ORDERS ||--o| SHIPMENTS : "order_id (1:0..1)"
    ORDERS ||--o{ RETURNS : "order_id"
    ORDERS ||--o{ REVIEWS : "order_id"
    
    %% Additional Links
    CUSTOMERS ||--o{ REVIEWS : "customer_id"
    PRODUCTS ||--o{ RETURNS : "product_id"
    PRODUCTS ||--o{ REVIEWS : "product_id"

    GEOGRAPHY {
        int zip PK
        string city
        string region
    }

    CUSTOMERS {
        int customer_id PK
        int zip FK
        string city
        date signup_date
    }

    PRODUCTS {
        int product_id PK
        string product_name
        string category
        float price
        float cogs
    }

    ORDERS {
        int order_id PK
        date order_date
        int customer_id FK
        int zip FK
        string order_status
    }

    ORDER_ITEMS {
        int order_id FK
        int product_id FK
        int quantity
        float unit_price
        string promo_id FK
    }

    PAYMENTS {
        int order_id PK, FK
        string payment_method
        float payment_value
    }

    SHIPMENTS {
        int order_id PK, FK
        date ship_date
        date delivery_date
    }

    RETURNS {
        string return_id PK
        int order_id FK
        int product_id FK
        string return_reason
    }

    REVIEWS {
        string review_id PK
        int order_id FK
        int product_id FK
        int customer_id FK
        int rating
    }

    INVENTORY {
        date snapshot_date PK
        int product_id PK, FK
        int stock_on_hand
        int units_sold
    }

    PROMOTIONS {
        string promo_id PK
        string promo_name
        string promo_type
        float discount_value
    }
```

### Chú thích:
- **PK**: Primary Key (Khoá chính)
- **FK**: Foreign Key (Khoá ngoại)
- **||--o{**: Quan hệ 1 - Nhiều (One to Many)
- **||--||**: Quan hệ 1 - 1 (One to One)
- **||--o|**: Quan hệ 1 - Không hoặc 1 (One to Zero or One)
