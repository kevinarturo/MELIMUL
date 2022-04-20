USE [MELI_DB];


DROP TABLE IF EXISTS [sites]
CREATE TABLE sites( 
    [id] VARCHAR(3), 
    [name] VARCHAR(20), 
    [default_currency_id] VARCHAR(3), 
    [enable] bit,
)

DROP TABLE IF EXISTS [searches]
CREATE TABLE [searches] (
    [id] int identity(1,1),
    [search] varchar(200),
    [enable] bit
)


DROP TABLE IF EXISTS [products]
CREATE TABLE [products] (
    [id] VARCHAR(50),
    [seller_id]  VARCHAR(100),
    [site_id] VARCHAR(3),
    [product_name] VARCHAR(500),
    [price] MONEY,
    [condition] VARCHAR(100),
    [thumbnail] VARCHAR(max),
    [accepts_mercadopago] BIT,
    [category_id] VARCHAR(100),
    [is_from_search] bit
)

DROP TABLE IF EXISTS [sellers]
CREATE TABLE [sellers](
    [id]  VARCHAR(100),
    [nickname] VARCHAR(250),
    [address] VARCHAR(250),

)

