
# DB EXAM

## Table of Contents

- [TODO](#todo)

- [Инициализация базы](#1-инициализация-базы)
- [продумать REST API](#2-продумать-rest-api)
- [заполнить бд большим количеством данных](#3-заполнить-бд-большим-количеством-данных)
- [составить разновидности запросов](#5-составить-разновидности-запросов)
- [использование ORM](#7-использование-orm)
- [использование пагинации](#8-использование-пагинации)
  

## 1. Инициализация базы

```
services:
	db:
		image: postgres:latest
```
указывается образ Docker (PostgreSQL)
```
		environment:
			- POSTGRES_DB=db
			- POSTGRES_USER=postgres
			- POSTGRES_PASSWORD=postgres
```

определяются переменные окружения для контейнера PostgreSQL
```
		healthcheck:
			test: ["CMD-SHELL", "pg_isready -U postgres"]
			interval: 10s
			timeout: 5s
			retries: 5
```
  мониторинг состояния базы данных
  

## 2. продумать REST API
  GET - возвращает все элементы/конкретный элемент от каждой модели
  POST -  добавляем элемент для каждой модели 
  PUT - меняем поле(я) для каждого элемента
  DELETE - удаляем элемент для каждой модели
  

## 3. заполнить бд большим количеством данных

`fill_database` заполняет базу данных случайными данными (компания, продукты и поставки), используя фиктивные данные с помощью библиотеки Faker и использует локальные CSV-файлы (`companies.csv`, `activity_types.csv`, `measurements.csv`, и `products.csv`).
  

## 4. ~~ миграции данных ~~

  

## 5. составить разновидности запросов
`/products&limit={limit_number}&page={page_number}&order_by={field_name}&asc={True|False}`
`/companies&...`
`/supplies&...`

возвращает продукты/компании/поставки, сортируя их по указанному полю, с пагинацией и возможностью изменения порядка сортировки


`/products/{product_id}` 
`/companies/{company_id}` 
`/supply/{supply_id}` 

возвращает продукт/компанию/поставку по ID


`/companies/total` 

возвращает компании со всеми продуктами и общей суммой продаж
  

## 6. ~~ pg_trgm + GIN ~~

## 7. использование ORM

```
class Company(SQLModel, table=True):
	company_id: int = Field(primary_key=True)
	name: str
	activity_type: str
	count_of_workers: int

class Product(SQLModel, table=True):
	product_id: int = Field(primary_key=True)
	product_name: str
	valid_until: Optional[datetime]
	measurement: str
	price: int

class Supplies(SQLModel, table=True):
	supply_id: int = Field(primary_key=True)
	company_id: int = Field(foreign_key="company.company_id")
	product_id: int = Field(foreign_key="product.product_id")
	date: Optional[datetime]
	size: int
	price: int
```

  
## 8. использование пагинации

```
def pagination_wrapper(results, limit: int, page: int):
	total = len(results)
	start = (page - 1) * limit
	end = start + limit
	paginated_results = results[start:end]
	return PaginationModel[T](
		limit=limit,
		page=page,
		results=paginated_results,
		total=total
	)
```
`result` - лист всех элементов

`limit` - максимальное число элементов на одной странице

`page` - номер страницы


`return` - возращает пагинированные элементы
  

## 9. ~~ создать простенький ui ~~

  

# TODO

1. [x] 5 баллов — написать скрипт инициализации базы (создание базы данных с определенным именем, установка владельца базы)

  
2. [x] 15 баллов — продумать REST API в зависимости от темы и написать программу, реализующую базовый CRUD


3. [x] 15 баллов - заполнить бд большим количеством данных с помощью скрипта, который взаимодействует с бд через REST API вашего приложения
  

4. [ ] 10 баллов — создать и добавить хотя бы 2 миграции данных (добавление новых колонок и построение индексов при помощи миграций)
  

5. [x] 5/25 баллов - составить следующие разновидности запросов, подходящих для вашей темы и реализовать их в виде вызовов REST API (по 5 баллов каждый):
-  - [x] SELECT ... WHERE (с несколькими условиями)
-  - [x] JOIN
-  - [x] UPDATE с нетривиальным условием
-  - [x] GROUP BY
-  - [x] добавить к параметрам запросов в API сортировку выдачи результатов по какому-то из полей


6. [ ] 20 баллов — создать JSON-поле, наполнить его данными, построить над ним pg_trgm + GIN индекс, реализовать полнотекстовый поиск по регулярному выражению из синтаксиса psql в виде REST API запроса


7. [x] 10 баллов - использование ORM


8. [x] 10 баллов - использование пагинации


9. [ ] 10 баллов - создать простенький ui