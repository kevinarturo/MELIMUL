USE [MELI_DB]
GO

INSERT INTO [MELI_DB].[dbo].[searches] ([search],[enable])
VALUES
 ('Celular iphone', 1)
,('Laptop toshiba', 0)
,('Carda para taladro', 0)

GO

INSERT INTO [MELI_DB].[dbo].[sites]([id],[name],[default_currency_id],[enable])
VALUES 
 ('MLM','Mexico','MXN',1)
,('MLA','Argentina','ARS',1)
,('MCR','Costa Rica','CRC',0)
,('MLV','Venezuela','VES',0)
,('MPY','Paraguay','PYG',0)
,('MLC','Chile','CLP',0)
,('MLU','Uruguay','UYU',0)
,('MPA','Panamá','PAB',0)
,('MRD','Dominicana','DOP',0)
,('MCU','Cuba','CUP',0)
,('MPE','Perú','PEN',0)
,('MCO','Colombia','COP',0)
,('MLB','Brasil','BRL',0)
,('MHN','Honduras','HNL',0)
,('MEC','Ecuador','USD',0)
,('MBO','Bolivia','BOB',0)
,('MSV','El Salvador','USD',0)
,('MNI','Nicaragua','NIO',0)
,('MGT','Guatemala','GTQ',0)