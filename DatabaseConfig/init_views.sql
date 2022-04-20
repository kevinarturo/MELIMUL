CREATE VIEW [dbo].[other_products_by_sellers]
AS
 SELECT T1.[id], T1.[nickname],
		T2.[product_name], T2.[price]
 FROM [dbo].[sellers] AS T1
 LEFT JOIN [dbo].[products] T2
 ON T1.[id] = T2.[seller_id]
 WHERE T2.[is_from_search] = 0