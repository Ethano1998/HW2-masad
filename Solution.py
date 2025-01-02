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
        conn.execute("CREATE TABLE Customers(cust_id INTEGER NOT NULL , full_name TEXT NOT NULL, "
                     " age INTEGER NOT NULL, phone TEXT NOT NULL, "
                     "CHECK (cust_id > 0), CHECK ( age >= 18 ), CHECK ( age <= 120), "
                     "CHECK ( LENGTH(phone) = 10 ), PRIMARY KEY(cust_id))")
        conn.execute("CREATE TABLE Orders(order_id INTEGER NOT NULL , date TIMESTAMP(0) NOT NULL, "
                     "delivery_fee DECIMAL NOT NULL, delivery_adress TEXT NOT NULL, "
                     "CHECK (order_id > 0), CHECK ( delivery_fee >= 0 ), "
                     "CHECK ( LENGTH(delivery_adress) >= 5 ), PRIMARY KEY(order_id))")
        conn.execute("CREATE TABLE Dishes(dish_id INTEGER NOT NULL , name TEXT NOT NULL, "
                     "price DECIMAL NOT NULL, is_active BOOLEAN NOT NULL, "
                     "CHECK (dish_id > 0), CHECK ( price > 0 ),CHECK (LENGTH(name) >= 4), PRIMARY KEY(dish_id))")
        conn.execute("CREATE TABLE CustomerPlacesOrder(cust_id INTEGER,order_id INTEGER, "
                     "PRIMARY KEY(order_id), "
                     "FOREIGN KEY (cust_id) REFERENCES Customers(cust_id) ON DELETE SET NULL, "
                     "FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE)")
        conn.execute("CREATE TABLE OrderContainsDish(order_id INTEGER,dish_id INTEGER,amount INTEGER NOT NULL,price DECIMAL NOT NULL, "
                     "PRIMARY KEY(order_id, dish_id), "
                     "FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE, "
                     "FOREIGN KEY (dish_id) REFERENCES Dishes(dish_id), "
                     "CHECK ( amount >= 0 ))")
        conn.execute("CREATE TABLE CustomerRatedDish(cust_id INTEGER NOT NULL, dish_id INTEGER NOT NULL, "
                     "rating INTEGER NOT NULL, CHECK ( rating >= 1 ), CHECK ( rating <= 5), "
                     "FOREIGN KEY (cust_id) REFERENCES Customers(cust_id) ON DELETE SET NULL, "
                     "FOREIGN KEY (dish_id) REFERENCES Dishes(dish_id), "
                     "PRIMARY KEY(cust_id, dish_id))")
        conn.execute("CREATE VIEW OrderTotalPrice AS "
                     "SELECT o.order_id, "
                     "SUM(coalesce((od.amount * od.price), 0)) + o.delivery_fee AS total_price, "
                     "(SELECT co.cust_id FROM CustomerPlacesOrder co WHERE co.order_id = o.order_id) AS cust_id "
                     "FROM Orders o LEFT OUTER JOIN OrderContainsDish od ON o.order_id = od.order_id "
                     "GROUP BY o.order_id")
        conn.execute("CREATE VIEW RatingDish AS "
                     "SELECT D.dish_id, "
                     "coalesce(AVG(C.rating), 3) AS avg_rating "
                     "FROM Dishes D "
                     "LEFT JOIN CustomerRatedDish C ON D.dish_id = C.dish_id "
                     "GROUP BY D.dish_id ")
        conn.execute("CREATE VIEW CustomerOrderedDish AS "
                     "SELECT  C.cust_id, O.dish_id "
                     "FROM CustomerPlacesOrder C, OrderContainsDish O "
                     "WHERE C.order_id = O.order_id AND C.cust_id IS NOT NULL ")
        conn.execute("CREATE VIEW AverageProfitPerOrderPerPrice AS "
                     "SELECT O.dish_id, O.price, (AVG(O.amount) * O.price) AS average_price "
                     "FROM OrderContainsDish O "
                     "GROUP BY O.price, O.dish_id")
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


def clear_tables() -> None:
    conn = None
    try:
        conn = Connector.DBConnector()
        conn.execute("DELETE FROM CustomerRatedDish")
        conn.execute("DELETE FROM OrderContainsDish")
        conn.execute("DELETE FROM CustomerPlacesOrder")
        conn.execute("DELETE FROM Dishes")
        conn.execute("DELETE FROM Orders")
        conn.execute("DELETE FROM Customers")
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


def drop_tables() -> None:
    conn = None
    try:
        conn = Connector.DBConnector()
        conn.execute("DROP VIEW IF EXISTS OrderTotalPrice")
        conn.execute("DROP VIEW IF EXISTS RatingDish")
        conn.execute("DROP VIEW IF EXISTS CustomerOrderedDish")
        conn.execute("DROP VIEW IF EXISTS AverageProfitPerOrderPerPrice")
        conn.execute("DROP TABLE IF EXISTS CustomerRatedDish CASCADE")
        conn.execute("DROP TABLE IF EXISTS OrderContainsDish CASCADE")
        conn.execute("DROP TABLE IF EXISTS CustomerPlacesOrder CASCADE")
        conn.execute("DROP TABLE IF EXISTS Dishes CASCADE")
        conn.execute("DROP TABLE IF EXISTS Orders CASCADE")
        conn.execute("DROP TABLE IF EXISTS Customers CASCADE")
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


# CRUD API

def add_customer(customer: Customer) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query= sql.SQL("INSERT INTO Customers(cust_id, full_name, age, phone) "
                       "VALUES ({cust_id}, {full_name}, {age}, {phone})").format(
            cust_id=sql.Literal(customer.get_cust_id()),
            full_name=sql.Literal(customer.get_full_name()),
            age=sql.Literal(customer.get_age()),
            phone=sql.Literal(customer.get_phone()))
        rows_effected, _ = conn.execute(query)
    except DatabaseException.ConnectionInvalid as e:
        print(e)
        return ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
        return ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
        return ReturnValue.ALREADY_EXISTS
    except Exception as e:
        print(e)
        return ReturnValue.BAD_PARAMS
    finally:
        conn.close()
    return ReturnValue.OK


def get_customer(customer_id: int) -> Customer:
    conn = None
    try:
        conn = Connector.DBConnector()
        query= sql.SQL("SELECT * FROM Customers WHERE cust_id = {customer_id}").format(
            customer_id=sql.Literal(customer_id))
        rows_effected, result = conn.execute(query)
        if rows_effected == 1:
            row = result.rows[0]
            customer = Customer(row[0], row[1], row[2], row[3])
        else :
            customer = BadCustomer()
    except DatabaseException.ConnectionInvalid as e:
        print(e)
        return BadCustomer()
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
        return BadCustomer()
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
        return BadCustomer()
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
        return BadCustomer()
    except Exception as e:
        print(e)
        return BadCustomer()
    finally:
        conn.close()
    return customer

def delete_customer(customer_id: int) -> ReturnValue:
   conn = None
   try:
       conn = Connector.DBConnector()
       query = sql.SQL("DELETE FROM Customers WHERE cust_id = {customer_id}").format(
           customer_id=sql.Literal(customer_id))
       rows_effected, _ = conn.execute(query)
       if rows_effected == 0:
            return ReturnValue.NOT_EXISTS
   except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
   except DatabaseException.NOT_NULL_VIOLATION:
       return ReturnValue.NOT_EXISTS
   except DatabaseException.CHECK_VIOLATION:
       return ReturnValue.NOT_EXISTS
   except DatabaseException.UNIQUE_VIOLATION:
       return ReturnValue.NOT_EXISTS
   except Exception:
       return ReturnValue.NOT_EXISTS
   finally:
       conn.close()
   return ReturnValue.OK

def add_order(order: Order) -> ReturnValue:
    conn = None
    try:
       conn = Connector.DBConnector()
       query =sql.SQL(
            "INSERT INTO Orders(order_id, date, delivery_fee, delivery_adress) "
            "VALUES({order_id}, {date}, {delivery_fee}, {delivery_adress})").format(
            order_id=sql.Literal(order.get_order_id()),
            date=sql.Literal(order.get_datetime()),
            delivery_fee=sql.Literal(order.get_delivery_fee()),
            delivery_adress=sql.Literal(order.get_delivery_address()))
       rows_effected, _ = conn.execute(query)
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION:
        return ReturnValue.ALREADY_EXISTS
    except Exception:
        return ReturnValue.BAD_PARAMS
    finally:
        conn.close()
    return ReturnValue.OK


def get_order(order_id: int) -> Order:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT * FROM Orders WHERE order_id = {order_id}").format(
            order_id=sql.Literal(order_id))
        rows_effected, result = conn.execute(query)
        if rows_effected == 1:
            row = result.rows[0]
            order = Order(row[0], row[1], row[2], row[3])
        else:
            order = BadOrder()
    except Exception:
        return BadOrder()
    finally:
        conn.close()
    return order


def delete_order(order_id: int) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM Orders WHERE order_id = {order_id}").format(
            order_id=sql.Literal(order_id))
        rows_effected, _ = conn.execute(query)
        if rows_effected == 0:
            return ReturnValue.NOT_EXISTS
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION:
        return ReturnValue.NOT_EXISTS
    except DatabaseException.CHECK_VIOLATION:
        return ReturnValue.NOT_EXISTS
    except DatabaseException.UNIQUE_VIOLATION:
        return ReturnValue.NOT_EXISTS
    except Exception:
        return ReturnValue.NOT_EXISTS
    finally:
        conn.close()
    return ReturnValue.OK


def add_dish(dish: Dish) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO Dishes(dish_id, name, price, is_active) "
                        "VALUES({dish_id}, {name}, {price}, {is_active})").format(
            dish_id=sql.Literal(dish.get_dish_id()),
            name=sql.Literal(dish.get_name()),
            price=sql.Literal(dish.get_price()),
            is_active=sql.Literal(dish.get_is_active()))
        rows_effected, _ = conn.execute(query)
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION:
        return ReturnValue.ALREADY_EXISTS
    except Exception:
        return ReturnValue.BAD_PARAMS
    finally:
        conn.close()
    return ReturnValue.OK


def get_dish(dish_id: int) -> Dish:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT * FROM Dishes WHERE dish_id = {dish_id}").format(
            dish_id =sql.Literal(dish_id))
        rows_effected, result = conn.execute(query)
        if rows_effected == 1:
            row = result.rows[0]
            dish = Dish(row[0], row[1], row[2], row[3])
        else :
            dish = BadDish()
    except Exception:
        return BadDish()
    finally:
        conn.close()
    return dish


def update_dish_price(dish_id: int, price: float) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("UPDATE Dishes SET price = {price} "
                        "WHERE dish_id = {dish_id} AND is_active = true").format(
            dish_id = sql.Literal(dish_id),
            price = sql.Literal(price))
        rows_effected, result = conn.execute(query)
        if rows_effected == 0:
            return ReturnValue.NOT_EXISTS
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION:
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION:
        return ReturnValue.NOT_EXISTS
    except Exception:
        return ReturnValue.BAD_PARAMS
    finally:
        conn.close()
    return ReturnValue.OK


def update_dish_active_status(dish_id: int, is_active: bool) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("UPDATE Dishes SET is_active = {is_active} "
                        "WHERE dish_id = {dish_id}").format(
            is_active=sql.Literal(is_active),
            dish_id=sql.Literal(dish_id))
        rows_effected, _ = conn.execute(query)
        if rows_effected == 0:
            return ReturnValue.NOT_EXISTS
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION:
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION:
        return ReturnValue.NOT_EXISTS
    except Exception:
        return ReturnValue.BAD_PARAMS
    finally:
        conn.close()
    return ReturnValue.OK


def customer_placed_order(customer_id: int, order_id: int) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO CustomerPlacesOrder(cust_id, order_id)"
                        " VALUES({cust_id}, {order_id})").format(
            cust_id=sql.Literal(customer_id),
            order_id=sql.Literal(order_id))
        rows_effected, _ = conn.execute(query)
        if rows_effected == 0:
            return ReturnValue.NOT_EXISTS
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION:
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION:
        return ReturnValue.NOT_EXISTS
    except Exception:
        return ReturnValue.ERROR
    finally:
        conn.close()
    return ReturnValue.OK


def get_customer_that_placed_order(order_id: int) -> Customer:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT C.cust_id, C.full_name, C.age, C.phone"
                        " FROM Customers C, CustomerPlacesOrder O"
                        " WHERE C.cust_id = O.cust_id AND O.order_id = {order_id}").format(
            order_id=sql.Literal(order_id))
        rows_effected, result = conn.execute(query)
        if rows_effected == 1:
            row = result.rows[0]
            customer = Customer(row[0], row[1], row[2], row[3])
        else:
            customer = BadCustomer()
    except Exception:
        return BadCustomer()
    finally:
        conn.close()
    return customer


def order_contains_dish(order_id: int, dish_id: int, amount: int) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO OrderContainsDish(order_id, dish_id, amount, price) "
                        "VALUES ({order_id},{dish_id},{amount}, "
                        "(SELECT price FROM Dishes WHERE dish_id = {dish_id} AND is_active = true))").format(
            order_id=sql.Literal(order_id),
            dish_id=sql.Literal(dish_id),
            amount=sql.Literal(amount))
        rows_effected, result = conn.execute(query)
        if rows_effected == 0:
            return ReturnValue.NOT_EXISTS
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION:
        return ReturnValue.NOT_EXISTS
    except DatabaseException.CHECK_VIOLATION:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION:
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION:
        return ReturnValue.NOT_EXISTS
    except Exception:
        return ReturnValue.NOT_EXISTS
    finally:
        conn.close()
    return ReturnValue.OK

def order_does_not_contain_dish(order_id: int, dish_id: int) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM OrderContainsDish "
                        "WHERE order_id = {order_id} AND dish_id = {dish_id}").format(
            order_id = sql.Literal(order_id),
            dish_id = sql.Literal(dish_id))
        rows_effected, result = conn.execute(query)
        if rows_effected == 0:
            return ReturnValue.NOT_EXISTS
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION:
        return ReturnValue.NOT_EXISTS
    except DatabaseException.CHECK_VIOLATION:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION:
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION:
        return ReturnValue.NOT_EXISTS
    except Exception:
        return ReturnValue.NOT_EXISTS
    finally:
        conn.close()
    return ReturnValue.OK


def get_all_order_items(order_id: int) -> List[OrderDish]:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT D.dish_id, O.amount, O.price "
                        "FROM Dishes D, OrderContainsDish O "
                        "WHERE D.dish_id = O.dish_id AND O.order_id = {order_id} "
                        "ORDER BY dish_id ASC").format(
            order_id=sql.Literal(order_id))
        rows_effected, result = conn.execute(query)
        dishes = []
        for i in range(rows_effected):
            row = result.rows[i]
            order_dish = OrderDish(row[0], row[1], row[2])
            dishes.append(order_dish)
    finally:
        conn.close()
    return dishes


def customer_rated_dish(cust_id: int, dish_id: int, rating: int) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO CustomerRatedDish(cust_id, dish_id, rating) "
                        "VALUES ({cust_id},{dish_id},{rating})").format(
            cust_id = sql.Literal(cust_id),
            dish_id = sql.Literal(dish_id),
            rating = sql.Literal(rating))
        rows_effected, result = conn.execute(query)
        if rows_effected == 0:
            return ReturnValue.NOT_EXISTS
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION:
        return ReturnValue.NOT_EXISTS
    except DatabaseException.CHECK_VIOLATION:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION:
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION:
        return ReturnValue.NOT_EXISTS
    except Exception:
        return ReturnValue.NOT_EXISTS
    finally:
        conn.close()
    return ReturnValue.OK


def customer_deleted_rating_on_dish(cust_id: int, dish_id: int) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM CustomerRatedDish "
                        "WHERE cust_id = {cust_id} AND dish_id = {dish_id}").format(
            cust_id = sql.Literal(cust_id),
            dish_id = sql.Literal(dish_id))
        rows_effected, result = conn.execute(query)
        if rows_effected == 0:
            return ReturnValue.NOT_EXISTS
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION:
        return ReturnValue.NOT_EXISTS
    except DatabaseException.CHECK_VIOLATION:
        return ReturnValue.NOT_EXISTS
    except DatabaseException.UNIQUE_VIOLATION:
        return ReturnValue.NOT_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION:
        return ReturnValue.NOT_EXISTS
    except Exception:
        return ReturnValue.NOT_EXISTS
    finally:
        conn.close()
    return ReturnValue.OK

def get_all_customer_ratings(cust_id: int) -> List[Tuple[int, int]]:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT D.dish_id, D.rating "
                        "FROM CustomerRatedDish D "
                        "WHERE D.cust_id = {cust_id} "
                        "ORDER BY dish_id ASC").format(
            cust_id=sql.Literal(cust_id))
        rows_effected, result = conn.execute(query)
        ratings = []
        for i in range(rows_effected):
            row = result.rows[i]
            rating = (row[0], row[1])
            ratings.append(rating)
    finally:
        conn.close()
    return ratings
# ---------------------------------- BASIC API: ----------------------------------

# Basic API


def get_order_total_price(order_id: int) -> float:
    # TODO: implement
    pass


def get_customers_spent_max_avg_amount_money() -> List[int]:
    # TODO: implement
    pass


def get_most_purchased_dish_among_anonymous_order() -> Dish:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT D.dish_id, D.name, D.price, D.is_active "
                        "FROM Dishes D, OrderContainsDish O "
                        "WHERE O.order_id NOT IN "
                        "(SELECT order_id FROM CustomerPlacesOrder C WHERE C.cust_id IS NOT NULL) "
                        "AND D.dish_id = O.dish_id "
                        "GROUP BY D.dish_id, D.name, D.price, D.is_active "
                        "ORDER BY SUM(O.amount) DESC, D.dish_id "
                        "LIMIT 1 ")
        rows_effected, result = conn.execute(query)
        row = result.rows[0]
        dish = Dish(row[0], row[1], row[2], row[3])
    finally:
        conn.close()
    return dish


def did_customer_order_top_rated_dishes(cust_id: int) -> bool:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT C.dish_id, TOP.avg_rating "
                        "FROM CustomerOrderedDish C, "
                        "(SELECT * FROM RatingDish ORDER BY avg_rating DESC, dish_id LIMIT 5) AS TOP "
                        "WHERE C.cust_id = {cust_id} AND C.dish_id = TOP.dish_id ").format(
            cust_id=sql.Literal(cust_id))
        rows_effected, result = conn.execute(query)
        if rows_effected != 0:
            return True
    finally:
        conn.close()
    return False


# ---------------------------------- ADVANCED API: ----------------------------------

# Advanced API


def get_customers_rated_but_not_ordered() -> List[int]:
    # TODO: implement
    pass


def get_non_worth_price_increase() -> List[int]:
    # TODO: implement
    pass


def get_cumulative_profit_per_month(year: int) -> List[Tuple[int, float]]:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("WITH RECURSIVE Months AS "
                        "(SELECT 1 AS month UNION ALL "
                        "SELECT month + 1 FROM Months WHERE month < 12), "
                        "MonthlyRevenue AS "
                        "(SELECT YEARORDER.month, SUM(P.total_price) AS revenue "
                        "FROM  OrderTotalPrice P, "
                        "(SELECT O.order_id, EXTRACT(MONTH FROM O.date) AS month FROM Orders O "
                        "WHERE EXTRACT(YEAR FROM O.date) = {year}) AS YEARORDER "
                        "WHERE YEARORDER.order_id = P.order_id "
                        "GROUP BY YEARORDER.month) "
                        "SELECT M.month, (SELECT coalesce(SUM(R.revenue), 0) FROM MonthlyRevenue R WHERE M.month >= R.month) "
                        "FROM Months M LEFT OUTER JOIN MonthlyRevenue R ON M.month = R.month "
                        "GROUP BY M.month "
                        "ORDER BY M.month DESC").format(
            year=sql.Literal(year))
        rows_effected, result = conn.execute(query)
        revenues = []
        for i in range(rows_effected):
            row = result.rows[i]
            revenue = (int(row[0]), float(row[1]))
            revenues.append(revenue)
    finally:
        conn.close()
    return revenues


def get_potential_dish_recommendations(cust_id: int) -> List[int]:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("WITH RECURSIVE SimilarCustomers AS "
                        "(SELECT {cust_id} AS cust_id UNION "
                        "SELECT C2.cust_id "
                        "FROM SimilarCustomers S JOIN CustomerRatedDish C ON S.cust_id = C.cust_id "
                        "JOIN CustomerRatedDish C2 ON C.dish_id = C2.dish_id "
                        "WHERE C.rating >= 4 AND C2.rating >= 4) "
                        "SELECT DISTINCT C.dish_id FROM SimilarCustomers S, CustomerRatedDish C "
                        "WHERE S.cust_id = C.cust_id "
                        "AND {cust_id} NOT IN (SELECT cust_id FROM CustomerOrderedDish D WHERE D.dish_id = C.dish_id) "
                        "ORDER BY dish_id").format(
            cust_id=sql.Literal(cust_id))
        rows_effected, result = conn.execute(query)
        dishes = []
        for i in range(rows_effected):
            row = result.rows[i]
            dishes.append(int(row[0]))
    finally:
        conn.close()
    return dishes

"""if __name__ == '__main__':
    def create_tabless() -> None:
        conn = None
        try:
            conn = Connector.DBConnector()
            conn.execute("CREATE TABLE Customers(cust_id INTEGER NOT NULL , full_name TEXT NOT NULL,"
                         " age INTEGER NOT NULL, phone TEXT NOT NULL,"
                         "CHECK (cust_id > 0), CHECK ( age >= 18 ), CHECK ( age <= 120),"
                         "CHECK ( LENGTH(phone) = 10 ), PRIMARY KEY(cust_id))")
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


    def dropTables() -> None:
        conn = None
        try:
            conn = Connector.DBConnector()
            conn.execute("DROP TABLE IF EXISTS Customers CASCADE")
        except DatabaseException.ConnectionInvalid as e:
            # do stuff
            print(e)
        except DatabaseException.NOT_NULL_VIOLATION as e:
            # do stuff
            print(e)
        except DatabaseException.CHECK_VIOLATION as e:
            # do stuff
            print(e)
        except DatabaseException.UNIQUE_VIOLATION as e:
            # do stuff
            print(e)
        except DatabaseException.FOREIGN_KEY_VIOLATION as e:
            # do stuff
            print(e)
        except Exception as e:
            print(e)
        finally:
            # will happen any way after code try termination or exception handling
            conn.close()
    create_tabless()
    add_customer(customer=Customer(cust_id=1, full_name="elie", age=26,phone="0585089585"))
    result = delete_customer(customer_id= 'elie')
    print(result)
    dropTables()
"""