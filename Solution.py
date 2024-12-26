from typing import List, Tuple
from psycopg2 import sql
from datetime import date, datetime
import Utility.DBConnector as Connector
from Utility.ReturnValue import ReturnValue
from Utility.Exceptions import DatabaseException
from Business.Customer import Customer, BadCustomer
from Business.Order import Order, BadOrder
from Business.Dish import Dish, BadDish
from Business.OrderDish import OrderDish


# ---------------------------------- CRUD API: ----------------------------------
# Basic database functions


def create_tables() -> None:
    conn = None
    try:
        conn = Connector.DBConnector()
        conn.execute("CREATE TABLE Customers(cust_id INTEGER NOT NULL , full_name TEXT NOT NULL,"
                     " age INTEGER NOT NULL, phone TEXT NOT NULL,"
                     "CHECK (cust_id > 0), CHECK ( age >= 18 ), CHECK ( age <= 120),"
                     "CHECK ( LENGTH(phone) = 10 ), PRIMARY KEY(cust_id))")
        conn.execute("CREATE TABLE Orders(order_id INTEGER NOT NULL , date TIMESTAMP(0) NOT NULL,"
                     "delivery_fee DECIMAL NOT NULL, delivery_adress TEXT NOT NULL,"
                     "CHECK (order_id > 0), CHECK ( delivery_fee >= 0 ),"
                     "CHECK ( LENGTH(delivery_adress) >= 5 ), PRIMARY KEY(order_id))")
        conn.execute("CREATE TABLE Dishes(dish_id INTEGER NOT NULL , name TEXT NOT NULL,"
                     "price DECIMAL NOT NULL, is_active BOOLEAN NOT NULL,"
                     "CHECK (dish_id > 0), CHECK ( price > 0 ),CHECK (LENGTH(name) >= 4), PRIMARY KEY(dish_id))")
        conn.execute("CREATE TABLE CustomerPlacesOrder(cust_id INTEGER,order_id INTEGER,"
                     "PRIMARY KEY(order_id),"
                     "FOREIGN KEY (cust_id) REFERENCES Customers(cust_id) ON DELETE SET NULL,"
                     "FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE)")
        conn.execute("CREATE TABLE OrderContainsDish(order_id INTEGER,dish_id INTEGER,amount INTEGER NOT NULL,price DECIMAL NOT NULL,"
                     "PRIMARY KEY(order_id, dish_id),"
                     "FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,"
                     "FOREIGN KEY (dish_id) REFERENCES Dishes(dish_id),"
                     "CHECK ( amount >= 0 ))")
        conn.execute("CREATE TABLE CustomerRatedDish (cust_id INTEGER NOT NULL, dish_id INTEGER NOT NULL,"
                     "rating INTEGER NOT NULL, CHECK ( rating >= 0 ), CHECK ( rating <= 5),"
                     "FOREIGN KEY (cust_id) REFERENCES Customers(cust_id) ON DELETE CASCADE,"
                     "FOREIGN KEY (dish_id) REFERENCES Dishes(dish_id),"
                     "PRIMARY KEY(cust_id, dish_id))")
        conn.execute("CREATE VIEW OrderTotalPrice AS "
                     "SELECT od.order_id,"
                     "SUM((od.amount * od.price) + (SELECT o.delivery_fee FROM Orders o WHERE o.order_id = od.order_id)) AS total_price,"
                     "(SELECT co.cust_id FROM CustomerPlacesOrder co WHERE co.order_id = od.order_id) AS cust_id"
                     "FROM OrderContainsDish od"
                     "GROUP BY od.order_id")
        conn.execute("CREATE VIEW RatingDish AS "
                     "SELECT dish_id,"
                     "AVG(rating) AS avg_rating"
                     "FROM CustomerRatedDish"
                     "GROUP BY dish_id")
        conn.execute("CREATE VIEW CustomerOrderedDish AS "
                     "SELECT  CustomerPlacesOrder.cust_id, OrderContainsDish.dish_id"
                     "FROM CustomerPlacesOrder, OrderContainsDish"
                     "WHERE CustomerPlacesOrder.order_id = OrderContainsDish.order_id")
        conn.execute("CREATE VIEW Average_profit_per_order_per_price AS "
                     "SELECT "
                     "FROM Dish, Order_contains_dish, "
                     "WHERE Customer_place_order.order_id = Order_contains_dish.order_id"
                     "GROUP BY")
    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        # will happen any way after try termination or exception handling
        conn.close()
    pass


def clear_tables() -> None:
    # TODO: implement
    pass


def drop_tables() -> None:
    # TODO: implement
    pass


# CRUD API

def add_customer(customer: Customer) -> ReturnValue:
    # TODO: implement
    pass


def get_customer(customer_id: int) -> Customer:
    # TODO: implement
    pass


def delete_customer(customer_id: int) -> ReturnValue:
    # TODO: implement
    pass


def add_order(order: Order) -> ReturnValue:
    # TODO: implement
    pass


def get_order(order_id: int) -> Order:
    # TODO: implement
    pass


def delete_order(order_id: int) -> ReturnValue:
    # TODO: implement
    pass


def add_dish(dish: Dish) -> ReturnValue:
    # TODO: implement
    pass


def get_dish(dish_id: int) -> Dish:
    # TODO: implement
    pass


def update_dish_price(dish_id: int, price: float) -> ReturnValue:
    # TODO: implement
    pass


def update_dish_active_status(dish_id: int, is_active: bool) -> ReturnValue:
    # TODO: implement
    pass


def customer_placed_order(customer_id: int, order_id: int) -> ReturnValue:
    # TODO: implement
    pass


def get_customer_that_placed_order(order_id: int) -> Customer:
    # TODO: implement
    pass


def order_contains_dish(order_id: int, dish_id: int, amount: int) -> ReturnValue:
    # TODO: implement
    pass


def order_does_not_contain_dish(order_id: int, dish_id: int) -> ReturnValue:
    # TODO: implement
    pass


def get_all_order_items(order_id: int) -> List[OrderDish]:
    # TODO: implement
    pass


def customer_rated_dish(cust_id: int, dish_id: int, rating: int) -> ReturnValue:
    # TODO: implement
    pass


def customer_deleted_rating_on_dish(cust_id: int, dish_id: int) -> ReturnValue:
    # TODO: implement
    pass

def get_all_customer_ratings(cust_id: int) -> List[Tuple[int, int]]:
    # TODO: implement
    pass
# ---------------------------------- BASIC API: ----------------------------------

# Basic API


def get_order_total_price(order_id: int) -> float:
    # TODO: implement
    pass


def get_customers_spent_max_avg_amount_money() -> List[int]:
    # TODO: implement
    pass


def get_most_purchased_dish_among_anonymous_order() -> Dish:
    # TODO: implement
    pass


def did_customer_order_top_rated_dishes(cust_id: int) -> bool:
    # TODO: implement
    pass


# ---------------------------------- ADVANCED API: ----------------------------------

# Advanced API


def get_customers_rated_but_not_ordered() -> List[int]:
    # TODO: implement
    pass


def get_non_worth_price_increase() -> List[int]:
    # TODO: implement
    pass


def get_cumulative_profit_per_month(year: int) -> List[Tuple[int, float]]:
    # TODO: implement
    pass


def get_potential_dish_recommendations(cust_id: int) -> List[int]:
    # TODO: implement
    pass
