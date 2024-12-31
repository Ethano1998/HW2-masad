import unittest
from datetime import datetime

import Solution as Solution
from Business.Dish import Dish, BadDish
from Business.Order import Order, BadOrder
from Business.OrderDish import OrderDish
from Utility.ReturnValue import ReturnValue
from Tests.AbstractTest import AbstractTest
from Business.Customer import Customer, BadCustomer

'''
    Simple test, create one of your own
    make sure the tests' names start with test
'''


class Test(AbstractTest):
    def test_customer(self) -> None:
        c1 = Customer(1, 'name', 21, "0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 1.1')
        c2 = Customer(2, None, 21, "Haifa")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c2), 'test 1.2') # full_name is NULL
        c3 = Customer(3, 'Yalla', 21, "Haifa")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c3), 'test 1.3') # len(phone) != 10
        c4 = Customer(4, 'name', 21, "0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c4), 'test 1.4')
        c5 = Customer(5, 'name', 21, "0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c5), 'test 1.5')
        c6 = Customer(6, 'name', 21, "0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c6), 'test 1.6')
        self.assertEqual(Customer(4, 'name', 21, "0123456789"),
                         Solution.get_customer(4), 'test 1.7')
        self.assertEqual(Customer(5, 'name', 21, "0123456789"),
                         Solution.get_customer(5), 'test 1.8')
        self.assertEqual(Customer(6, 'name', 21, "0123456789"),
                         Solution.get_customer(6), 'test 1.9')
        self.assertEqual(Customer(1, 'name', 21, "0123456789"),
                         Solution.get_customer(1), 'test 1.10')
        Solution.delete_customer(4)
        self.assertEqual(BadCustomer(), Solution.get_customer(4), 'test 1.11')
        Solution.delete_customer(5)
        self.assertEqual(BadCustomer(), Solution.get_customer(5), 'test 1.12')
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.add_customer(c1), 'test 1.13')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.delete_customer(30), 'test 1.14')
        c7 = Customer(-1, 'name', 21, "0123456789")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c7), 'test 1.15') # cust_id < 0
        c8 = Customer(8, 'name', 2, "0123456789")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c8), 'test 1.16') # age < 18
        c9 = Customer(9, 'name', 2221, "0123456789")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c9), 'test 1.17') # age > 120
        c10 = Customer(None, 'name', 2221, "0123456789")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c10), 'test 1.18') # cust_id is NULL
        c11 = Customer(11, 'name', None, "0123456789")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c11), 'test 1.19') # age is NULL
        c12 = Customer(12, 'name', 21, None)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c12), 'test 1.20') # phone is NULL



    def test_order(self) -> None:
        o1 = Order(1, datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   21, "address 1")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 2.1')
        o2 = Order(1, datetime(year=3400, month=12, day=31, hour=23, minute=1, second=23),
                   21, "address 1")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.add_order(o2), 'test 2.2')
        o3 = Order(3, datetime(year=2055, month=12, day=31, hour=23, minute=1, second=23),
                   11, "address 1")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 2.3')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.delete_order(777), 'test 2.4')
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.add_order(o1), 'test 2.5')
        self.assertEqual(ReturnValue.OK, Solution.delete_order(3), 'test 2.6')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.delete_order(3), 'test 2.7')
        self.assertEqual(Order(1, datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                               21, "address 1"), Solution.get_order(1), 'test 2.8')
        o4 = Order(4, datetime(year=1896, month=12, day=31, hour=23, minute=1, second=23),
                   11, "address 1")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 3.1')
        self.assertEqual(ReturnValue.OK, Solution.delete_order(4), 'test 3.2')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.delete_order(4), 'test 3.3')
        o5 = Order(None, datetime(year=1990, month=12, day=31, hour=23, minute=1, second=23),
                   11, "address 1")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_order(o5), 'test 3.4') # order_id is NULL
        o6 = Order(order_id=-333, date=datetime(year=1900, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=3, delivery_address="barber 1")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_order(o6), 'test 3.5') # order_id < 0
        o7 = Order(order_id=7, date=datetime(year=1900, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=-333, delivery_address="blabla 1")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_order(o7), 'test 3.6') # delivery_fee < 0
        o8 = Order(order_id=8, date=datetime(year=1900, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=0, delivery_address=None)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_order(o8), 'test 3.7') # delivery_address is NULL
        o9 = Order(order_id=9, date=datetime(year=1900, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=None, delivery_address="blabla 1")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_order(o9), 'test 3.8') # delivery_fee is NULL
        self.assertEqual(BadOrder(), Solution.get_order(99999), 'test 3.9')
        o10 = Order(order_id=10, date=datetime(year=1900, month=12, day=31, hour=23, minute=1, second=23),
                    delivery_fee=77, delivery_address="1")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_order(o10), 'test 3.9') # len(deliver_address) < 5
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 3.10')
        self.assertEqual(Order(4, datetime(year=1896, month=12, day=31, hour=23, minute=1, second=23),
                               11, "address 1"), Solution.get_order(4), 'test 3.11')



    def test_dish(self) -> None:
        d1 = Dish(dish_id=None, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d1), 'test 4.1') # dish_id is NULL
        d2 = Dish(dish_id=2, name=None, price=1, is_active=True)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d2), 'test 4.2') # name is NULL
        d3 = Dish(dish_id=3, name='100000', price=None, is_active=True)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d3), 'test 4.3') # price is NULL
        d4 = Dish(dish_id=4, name='1000000', price=3, is_active=None)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d4), 'test 4.4') # is_active is NULL
        d5 = Dish(dish_id=-66666, name='100000', price=7, is_active=True)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d5), 'test 4.5') # dish_id < 0
        d6 = Dish(dish_id=15, name='100000', price=-777777777, is_active=True)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d6), 'test 4.6') # price < 0
        d7 = Dish(dish_id=7, name='100000', price=0, is_active=True)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d7), 'test 4.7') # price == 0
        d8 = Dish(dish_id=8, name='1', price=8, is_active=True)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d8), 'test 4.8') # len(name) < 4
        d9 = Dish(dish_id=9, name='1111', price=9, is_active=False)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d9), 'test 4.9')
        d10 = Dish(dish_id=10, name='1111111', price=10, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d10), 'test 4.10')
        self.assertEqual(d9, Solution.get_dish(9), 'test 4.11')
        self.assertEqual(d10, Solution.get_dish(10), 'test 4.12')
        self.assertEqual(BadDish(), Solution.get_dish(99999), 'test 4.13')
        self.assertEqual(ReturnValue.OK, Solution.update_dish_price(10, 50), 'test 4.14')
        _d10 = Dish(dish_id=10, name='1111111', price=50, is_active=True)
        self.assertEqual(_d10, Solution.get_dish(10), 'test 4.15')
        d11 = Dish(dish_id=11, name='1111111', price=10, is_active=False)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d11), 'test 4.16')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.update_dish_price(11, 30), 'test 4.17') # is_active = False
        self.assertEqual(ReturnValue.BAD_PARAMS,
                         Solution.update_dish_price(10, -1), 'test 4.18') # price < 0
        self.assertEqual(ReturnValue.OK,
                         Solution.update_dish_active_status(10, False), 'test 4.19')
        _d10.set_is_active(False)
        self.assertEqual(_d10, Solution.get_dish(10), 'test 4.20')
        _d10.set_is_active(True)
        self.assertEqual(ReturnValue.OK, Solution.update_dish_active_status(10, True), 'test 4.21')
        self.assertEqual(_d10, Solution.get_dish(10), 'test 4.22')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.update_dish_active_status(434343, True),'test 4.23')



    def test_clear_tables(self) -> None:
        c = Customer(10, 'name', 22, "0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c), 'test 5.1')
        o = Order(10, datetime(year=2055, month=12, day=31, hour=23, minute=1, second=23),
                  11, "address 1")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o), 'test 5.2')
        d = Dish(dish_id=10, name='1111111', price=10, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d), 'test 5.3')
        self.assertEqual(c, Solution.get_customer(10), 'test 5.4')
        self.assertEqual(o, Solution.get_order(10), 'test 5.5')
        self.assertEqual(d, Solution.get_dish(10), 'test 5.6')
        Solution.clear_tables()
        self.assertEqual(BadCustomer(), Solution.get_customer(10), 'test 5.7')
        self.assertEqual(BadOrder(), Solution.get_order(10), 'test 5.8')
        self.assertEqual(BadDish(), Solution.get_dish(10), 'test 5.9')



    def test_customer_order(self) -> None:
        c1 = Customer(cust_id=1, full_name='1', age=22, phone="0123456789")
        c2 = Customer(cust_id=2, full_name='2', age=22, phone="0123456789")
        c3 = Customer(cust_id=3, full_name='3', age=22, phone="0123456789")
        c4 = Customer(cust_id=4, full_name='4', age=22, phone="0123456789")
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 6.1')
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2), 'test 6.2')
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c3), 'test 6.3')
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c4), 'test 6.4')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 6.5')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 6.6')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 6.7')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1,1), 'test 6.8')
        self.assertEqual(ReturnValue.ALREADY_EXISTS,
                         Solution.customer_placed_order(1, 1), 'test 6.9')
        self.assertEqual(ReturnValue.ALREADY_EXISTS,
                         Solution.customer_placed_order(2, 1), 'test 6.10')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.customer_placed_order(5, 5), 'test 6.11')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.customer_placed_order(5, 2), 'test 6.12')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.customer_placed_order(2, 5), 'test 6.13')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(2, 2), 'test 6.14')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(3, 3), 'test 6.15')
        o4 = Order(order_id=4, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 6.16')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1, 4), 'test 6.17')
        self.assertEqual(ReturnValue.ALREADY_EXISTS,
                         Solution.customer_placed_order(2, 4), 'test 6.18')
        ###################################
        ### get_customer_that_placed_order:
        ###################################
        self.assertEqual(Customer(cust_id=2, full_name='2', age=22, phone="0123456789"),
                         Solution.get_customer_that_placed_order(2), 'test 6.19')
        self.assertEqual(Customer(cust_id=3, full_name='3', age=22, phone="0123456789"),
                         Solution.get_customer_that_placed_order(3), 'test 6.20')
        self.assertEqual(BadCustomer(), Solution.get_customer_that_placed_order(898989), 'test 6.21')



    def test_order_contains_dish(self) -> None:
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 7.1')
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 7.2')
        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 7.3')
        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 7.4')
        d2 = Dish(dish_id=2, name='yummy', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 7.5')
        d3 = Dish(dish_id=3, name='100000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 7.6')
        d4 = Dish(dish_id=4, name='1000000', price=3, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 7.7')
        d5 = Dish(dish_id=5, name='100000', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 7.8')
        d6 = Dish(dish_id=6, name='100000', price=77, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d6), 'test 7.9')
        d7 = Dish(dish_id=7, name='100000', price=11, is_active=False)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d7), 'test 7.10')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=1, dish_id=1, amount=3), 'test 7.11')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=1, dish_id=2, amount=10), 'test 7.12')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=2, dish_id=1, amount=30), 'test 7.13')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=2, dish_id=2, amount=101), 'test 7.14')
        self.assertEqual(ReturnValue.ALREADY_EXISTS,
                         Solution.order_contains_dish(order_id=1, dish_id=1, amount=3), 'test 7.15')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.order_contains_dish(order_id=1, dish_id=7, amount=3),'test 7.16')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.order_contains_dish(order_id=10, dish_id=2, amount=3), 'test 7.17')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.order_contains_dish(order_id=10, dish_id=7, amount=3), 'test 7.18')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.order_contains_dish(order_id=10, dish_id=1, amount=3), 'test 7.19')
        self.assertEqual(ReturnValue.OK,
                         Solution.update_dish_active_status(dish_id=7, is_active=True), 'test 7.20')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=1, dish_id=7, amount=10), 'test 7.21')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=3, dish_id=7, amount=10), 'test 7.22')
        self.assertEqual(ReturnValue.BAD_PARAMS,
                         Solution.order_contains_dish(order_id=2, dish_id=4, amount=-333), 'test 7.23')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=1, dish_id=5, amount=10), 'test 7.24')
        self.assertEqual(ReturnValue.OK,
                         Solution.update_dish_active_status(dish_id=5, is_active=False), 'test 7.25')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.order_contains_dish(order_id=2, dish_id=5, amount=3), 'test 7.26')
        self.assertEqual(ReturnValue.OK,
                         Solution.update_dish_active_status(dish_id=5, is_active=True), 'test 7.27')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=2, dish_id=5, amount=3), 'test 7.28')
        ################################
        ### order_does_not_contain_dish:
        ################################
        self.assertEqual(ReturnValue.ALREADY_EXISTS,
                         Solution.order_contains_dish(order_id=1, dish_id=1, amount=3), 'test 7.29')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_does_not_contain_dish(order_id=1, dish_id=1), 'test 7.30')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(order_id=1, dish_id=1, amount=5), 'test 7.31')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.order_does_not_contain_dish(order_id=1, dish_id=222), 'test 7.32')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.order_does_not_contain_dish(order_id=2222, dish_id=1), 'test 7.33')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.order_does_not_contain_dish(order_id=2222, dish_id=222), 'test 7.34')



    def test_get_all_order_items(self) -> None:
        # setup: insert orders o1 - o4, dishes d1 - d7.
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 8.1')
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 8.2')
        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 8.3')
        o4 = Order(order_id=4, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=21, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 8.4')
        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 8.5')
        d2 = Dish(dish_id=2, name='yummy', price=2, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 8.6')
        d3 = Dish(dish_id=3, name='100000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 8.7')
        d4 = Dish(dish_id=4, name='1000000', price=3, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 8.8')
        d5 = Dish(dish_id=5, name='100000', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 8.9')
        d6 = Dish(dish_id=6, name='100000', price=77, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d6), 'test 8.10')
        d7 = Dish(dish_id=7, name='100000', price=11, is_active=False)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d7), 'test 8.11')
        # add dishes to orders - o1 = { (dish_id=1, amount=2, price=1), (dish_id=2, amount=1, price=2) }
        #                        o2 = { }
        #                        o3 = { (dish_id=1, amount=5, price=1), (dish_id=3, amount=1, price=1),
        #                               (dish_id=4, amount=3, price=3), (dish_id=5, amount=7, price=7) }
        #                        o4 = { }
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(1,1,2), 'test 8.12')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(1, 2, 1), 'test 8.13')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 1, 5), 'test 8.14')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 3, 1), 'test 8.15')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 4, 3), 'test 8.16')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 5, 7), 'test 8.17')
        o1_items = [OrderDish(1, 2, 1), OrderDish(2, 1, 2)]
        o2_items = []
        o3_items = [OrderDish(1, 5, 1), OrderDish(3, 1, 1),
                    OrderDish(4, 3, 3), OrderDish(5, 7, 7)]
        o4_items = []
        self.assertEqual(o1_items, Solution.get_all_order_items(order_id=1), 'test 8.18')
        self.assertEqual(o2_items, Solution.get_all_order_items(order_id=2), 'test 8.19')
        self.assertEqual(o3_items, Solution.get_all_order_items(order_id=3), 'test 8.20')
        self.assertEqual(o4_items, Solution.get_all_order_items(order_id=4), 'test 8.21')
        # remove some dishes:
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(order_id=1, dish_id=2), 'test 8.22')
        o1_items = [OrderDish(1, 2, 1)]
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(order_id=3, dish_id=1), 'test 8.23')
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(order_id=3, dish_id=5), 'test 8.24')
        o3_items = [OrderDish(3, 1, 1), OrderDish(4, 3, 3)]
        self.assertEqual(o1_items, Solution.get_all_order_items(order_id=1), 'test 8.25')
        self.assertEqual(o3_items, Solution.get_all_order_items(order_id=3), 'test 8.26')



    def test_customer_rated_dish(self) -> None:
        c1 = Customer(cust_id=1, full_name='1', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 9.1')
        c2 = Customer(cust_id=2, full_name='2', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2), 'test 9.2')
        c3 = Customer(cust_id=3, full_name='3', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c3), 'test 9.3')
        c4 = Customer(cust_id=4, full_name='4', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c4), 'test 9.4')
        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 9.5')
        d2 = Dish(dish_id=2, name='yummy', price=2, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 9.6')
        d3 = Dish(dish_id=3, name='100000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 9.7')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(cust_id=1, dish_id=1, rating=1), 'test 9.8')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(cust_id=2, dish_id=1, rating=2), 'test 9.9')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(cust_id=3, dish_id=1, rating=3), 'test 9.10')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(cust_id=1, dish_id=2, rating=1), 'test 9.11')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(cust_id=2, dish_id=2, rating=2), 'test 9.12')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(cust_id=3, dish_id=2, rating=3), 'test 9.13')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(cust_id=4, dish_id=1, rating=4), 'test 9.14')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(cust_id=4, dish_id=2, rating=5), 'test 9.15')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(cust_id=4, dish_id=3, rating=2), 'test 9.16')
        self.assertEqual(ReturnValue.BAD_PARAMS,
                         Solution.customer_rated_dish(cust_id=1, dish_id=3, rating=111), 'test 9.17')
        self.assertEqual(ReturnValue.BAD_PARAMS,
                         Solution.customer_rated_dish(cust_id=1, dish_id=3, rating=0), 'test 9.18')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.customer_rated_dish(cust_id=1, dish_id=3333, rating=4), 'test 9.19')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.customer_rated_dish(cust_id=123123, dish_id=3, rating=4), 'test 9.20')
        self.assertEqual(ReturnValue.ALREADY_EXISTS,
                         Solution.customer_rated_dish(cust_id=1, dish_id=1, rating=1), 'test 9.21')
        self.assertEqual(ReturnValue.ALREADY_EXISTS,
                         Solution.customer_rated_dish(cust_id=1, dish_id=1, rating=3), 'test 9.22')
        ####################################
        ### customer_deleted_rating_on_dish:
        ####################################
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_deleted_rating_on_dish(cust_id=1, dish_id=1), 'test 9.23')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_rated_dish(cust_id=1, dish_id=1, rating=5), 'test 9.24')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_deleted_rating_on_dish(cust_id=1, dish_id=1), 'test 9.25')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.customer_deleted_rating_on_dish(cust_id=1, dish_id=1), 'test 9.26')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.customer_deleted_rating_on_dish(cust_id=1111, dish_id=1), 'test 9.27')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.customer_deleted_rating_on_dish(cust_id=1, dish_id=1111), 'test 9.28')
        self.assertEqual(ReturnValue.NOT_EXISTS,
                         Solution.customer_deleted_rating_on_dish(cust_id=1111, dish_id=1111), 'test 9.29')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_rated_dish(cust_id=1, dish_id=1, rating=2), 'test 9.30')
        #############################
        ### get_all_customer_ratings:
        #############################
        # current rating are:
        c1_ratings = [(1, 2), (2, 1)]
        c2_ratings = [(1, 2), (2, 2)]
        c3_ratings = [(1, 3), (2, 3)]
        c4_ratings = [(1, 4), (2, 5), (3, 2)]
        self.assertEqual(c1_ratings, Solution.get_all_customer_ratings(1), 'test 9.31')
        self.assertEqual(c2_ratings, Solution.get_all_customer_ratings(2), 'test 9.32')
        self.assertEqual(c3_ratings, Solution.get_all_customer_ratings(3), 'test 9.33')
        self.assertEqual(c4_ratings, Solution.get_all_customer_ratings(4), 'test 9.34')
        # delete c1's ratings:
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_deleted_rating_on_dish(cust_id=1, dish_id=1), 'test 9.35')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_deleted_rating_on_dish(cust_id=1, dish_id=2), 'test 9.36')
        self.assertEqual([], Solution.get_all_customer_ratings(1), 'test 9.37')
        # mix-up order of ratings to check ORDER BY dish_id:
        d4 = Dish(dish_id=4, name='100000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 9.38')
        d5 = Dish(dish_id=5, name='100000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 9.39')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_rated_dish(cust_id=1, dish_id=5, rating=1), 'test 9.40')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_rated_dish(cust_id=1, dish_id=2, rating=4), 'test 9.41')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_rated_dish(cust_id=1, dish_id=3, rating=2), 'test 9.42')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_rated_dish(cust_id=1, dish_id=1, rating=2), 'test 9.43')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_rated_dish(cust_id=1, dish_id=4, rating=5), 'test 9.44')
        c1_ratings = [(1, 2), (2, 4), (3, 2), (4, 5), (5, 1)]
        self.assertEqual(c1_ratings, Solution.get_all_customer_ratings(1), 'test 9.45')



    def test_get_order_total_price(self) -> None:
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 10.1')
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=2, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 10.2')
        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=3, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 10.3')
        o4 = Order(order_id=4, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=4, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 10.4')
        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 10.5')
        d2 = Dish(dish_id=2, name='yummy', price=2, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 10.6')
        d3 = Dish(dish_id=3, name='100000', price=3, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 10.7')
        d4 = Dish(dish_id=4, name='1000000', price=4, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 10.8')
        d5 = Dish(dish_id=5, name='100000', price=5, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 10.9')
        d6 = Dish(dish_id=6, name='100000', price=6, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d6), 'test 10.10')
        d7 = Dish(dish_id=7, name='100000', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d7), 'test 10.11')
        # order total prices include only delivery_fee:
        self.assertEqual(1, Solution.get_order_total_price(1), 'test 10.12')
        self.assertEqual(2, Solution.get_order_total_price(2), 'test 10.13')
        self.assertEqual(3, Solution.get_order_total_price(3), 'test 10.14')
        # add dishes to orders:
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1,1,1), 'test 10.15')
        self.assertEqual(1 + 1, Solution.get_order_total_price(1), 'test 10.16')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(1, 2, 2), 'test 10.16')
        self.assertEqual(1 + 1 + (2 * 2), Solution.get_order_total_price(1), 'test 10.17')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 1, 1), 'test 10.18')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 2, 1), 'test 10.19')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 3, 1), 'test 10.20')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 4, 1), 'test 10.21')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 5, 1), 'test 10.22')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 6, 1), 'test 10.23')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 7, 1), 'test 10.24')
        self.assertEqual(2 + 1 + 2 + 3 + 4 + 5 + 6 + 7, Solution.get_order_total_price(2), 'test 10.25')
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(2, 3), 'test 10.26')
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(2, 6), 'test 10.27')
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(2, 1), 'test 10.28')
        self.assertEqual(2 + 2 + 4 + 5 + 7, Solution.get_order_total_price(2), 'test 10.29')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 1, 777), 'test 10.30')
        self.assertEqual(3 + 777, Solution.get_order_total_price(3), 'test 10.31')
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(3, 1), 'test 10.32')
        self.assertEqual(3, Solution.get_order_total_price(3), 'test 10.33')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 1, 444), 'test 10.34')
        self.assertEqual(3 + 444, Solution.get_order_total_price(3), 'test 10.35')



    def test_get_customers_spent_max_avg_amount_money(self) -> None:
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 11.1')
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=2, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 11.2')
        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=3, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 11.3')
        o4 = Order(order_id=4, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=4, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 11.4')
        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 11.5')
        d2 = Dish(dish_id=2, name='yummy', price=2, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 11.6')
        d3 = Dish(dish_id=3, name='100000', price=3, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 11.7')
        d4 = Dish(dish_id=4, name='1000000', price=4, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 11.8')
        d5 = Dish(dish_id=5, name='100000', price=5, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 11.9')
        d6 = Dish(dish_id=6, name='100000', price=6, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d6), 'test 11.10')
        d7 = Dish(dish_id=7, name='100000', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d7), 'test 11.11')
        c1 = Customer(cust_id=1, full_name='1', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 11.12')
        c2 = Customer(cust_id=2, full_name='2', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2), 'test 11.13')
        c3 = Customer(cust_id=3, full_name='3', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c3), 'test 11.14')
        c4 = Customer(cust_id=4, full_name='4', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c4), 'test 11.15')
        max_spenders = []
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.16')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1,1), 'test 11.17')
        max_spenders = [1]
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.18')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(1, 1, 4), 'test 11.19')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 2, 1), 'test 11.20')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1, 2), 'test 11.21')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 3, 1), 'test 11.22')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(2, 3), 'test 11.23')
        max_spenders = [2] # c1 spent (delivery = )1 + (price*amount = )4 on o1,
        # (delivery = )2 + (price*amount = )2 on o2,
        # so (5 + 4) / 2 = 4.5, while c2 spent (delivery)3 + (price*amount)3 on o3
        # so c1's avg spending is 4.5 < c2's avg spending = 6
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.24')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1, 4), 'test 11.25')
        # now c1 spent even less on average (total of o4 is only delivery_fee, which is 4)
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.26')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(4, 1, 5), 'test 11.27')
        # now c1 spent total(o1) + total(o2) + total(o4) = 5 + 4 + 9
        # and so average_spending(c1) = 18 / 3 = 6 = average_spending(c2)
        max_spenders = [1, 2]
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.28')
        o44 = Order(order_id=44, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=4, delivery_address="address") # notice that delivery_fee == 4, not 44
        self.assertEqual(ReturnValue.OK, Solution.add_order(o44), 'test 11.29')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(3, 44), 'test 11.30')
        # no change in max_spenders
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.31')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(44, 1, 2), 'test 11.32')
        # add c3 to max_spenders
        max_spenders = [1, 2, 3]
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.33')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(44, 2, 1), 'test 11.34')
        # c3 placed order o4
        max_spenders = [3]
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.35')
        self.assertEqual(ReturnValue.OK, Solution.delete_customer(3), 'test 11.36')
        max_spenders = [1, 2]
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(),'test 11.37')
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c3), 'test 11.38')
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.39')
        o5 = Order(order_id=5, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=5, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o5), 'test 11.40')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(5, 1, 1), 'test 11.41')
        # total(o5) = 5 + 1 = 6
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(3, 5), 'test 11.42')
        max_spenders = [1, 2, 3]
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.43')
        self.assertEqual(ReturnValue.OK, Solution.delete_customer(2), 'test 11.44')
        max_spenders = [1, 3]
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.45')
        o11 = Order(order_id=11, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address") # note that delivery_fee of o11 is 1, not 11
        self.assertEqual(ReturnValue.OK, Solution.add_order(o11), 'test 11.46')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_placed_order(1, 11), 'test 11.47')
        # now average_spending(c1) < average_spending(c3)
        max_spenders = [3]
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.48')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(11, 1, 5), 'test 11.49')
        # and again average_spending(c1) = average_spending(c3) = 6
        max_spenders = [1, 3]
        self.assertEqual(max_spenders, Solution.get_customers_spent_max_avg_amount_money(), 'test 11.50')
        #
        # NOTE: MAKE MORE COMPREHENSIVE TESTS
        #

    def test_get_most_purchased_dish_among_anonymous_order(self) -> None:
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 12.1')
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=2, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 12.2')
        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=3, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 12.3')
        o4 = Order(order_id=4, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=4, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 12.4')
        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 12.5')
        d2 = Dish(dish_id=2, name='yummy', price=2, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 12.6')
        d3 = Dish(dish_id=3, name='100000', price=3, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 12.7')
        d4 = Dish(dish_id=4, name='1000000', price=4, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 12.8')
        d5 = Dish(dish_id=5, name='100000', price=5, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 12.9')
        d6 = Dish(dish_id=6, name='100000', price=6, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d6), 'test 12.10')
        d7 = Dish(dish_id=7, name='100000', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d7), 'test 12.11')
        c1 = Customer(cust_id=1, full_name='1', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 12.12')
        c2 = Customer(cust_id=2, full_name='2', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2), 'test 12.13')
        c3 = Customer(cust_id=3, full_name='3', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c3), 'test 12.14')
        c4 = Customer(cust_id=4, full_name='4', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c4), 'test 12.15')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 2, 2), 'test 12.16')
        self.assertEqual(Dish(dish_id=2, name='yummy', price=2, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.17')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(1, 1, 1), 'test 12.18')
        self.assertEqual(Dish(dish_id=2, name='yummy', price=2, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.19')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 2, 1), 'test 12.20')
        self.assertEqual(Dish(dish_id=2, name='yummy', price=2, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.21')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 1, 2), 'test 12.22')
        self.assertEqual(Dish(dish_id=1, name='10000', price=1, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.23')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1,1), 'test 12.24')
        self.assertEqual(Dish(dish_id=2, name='yummy', price=2, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.25')
        self.assertEqual(ReturnValue.OK, Solution.delete_customer(1), 'test 12.26')
        # o1 does not belong to c1 anymore
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 12.27')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(1, 3, 1), 'test 12.28')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 3, 1), 'test 12.29')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 3, 1), 'test 12.30')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(4, 3, 1), 'test 12.31')
        self.assertEqual(Dish(dish_id=3, name='100000', price=3, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.32')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(3, 3), 'test 12.33')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(4,4,1), 'test 12.34')
        self.assertEqual(Dish(dish_id=4, name='1000000', price=4, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.35')
        self.assertEqual(ReturnValue.OK, Solution.delete_order(1), 'test 12.36')
        o2_dishes = [OrderDish(2, 2, 2), OrderDish(3, 1, 3)]
        o3_dishes = [OrderDish(1, 2, 1), OrderDish(2, 1, 2),
                    OrderDish(3, 1, 3)]
        o4_dishes = [OrderDish(3, 1, 3), OrderDish(4, 1, 4)]
        self.assertEqual(o2_dishes, Solution.get_all_order_items(2),'test 12.37')
        self.assertEqual(o3_dishes, Solution.get_all_order_items(3), 'test 12.38')
        self.assertEqual(o4_dishes, Solution.get_all_order_items(4), 'test 12.39')
        self.assertEqual(Dish(dish_id=4, name='1000000', price=4, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.40')
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(3, 3), 'test 12.41')
        self.assertEqual(Dish(dish_id=3, name='100000', price=3, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.42')
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(3, 2), 'test 12.43')
        self.assertEqual(Dish(dish_id=2, name='yummy', price=2, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.44')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(4, 2), 'test 12.45')
        self.assertEqual(Dish(dish_id=4, name='1000000', price=4, is_active=True),
                         Solution.get_most_purchased_dish_among_anonymous_order(), 'test 12.46')
        #
        # NOTE: MAKE MORE COMPREHENSIVE TESTS
        #

    def test_did_customer_order_top_rated_dishes(self) -> None:
        o1 = Order(order_id=1, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=1, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'test 13.1')
        o2 = Order(order_id=2, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=2, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'test 13.2')
        o3 = Order(order_id=3, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=3, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'test 13.3')
        o4 = Order(order_id=4, date=datetime(year=1000, month=12, day=31, hour=23, minute=1, second=23),
                   delivery_fee=4, delivery_address="address")
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'test 13.4')
        d1 = Dish(dish_id=1, name='10000', price=1, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'test 13.5')
        d2 = Dish(dish_id=2, name='yummy', price=2, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'test 13.6')
        d3 = Dish(dish_id=3, name='100000', price=3, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'test 13.7')
        d4 = Dish(dish_id=4, name='1000000', price=4, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'test 13.8')
        d5 = Dish(dish_id=5, name='100000', price=5, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'test 13.9')
        d6 = Dish(dish_id=6, name='100000', price=6, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d6), 'test 13.10')
        d7 = Dish(dish_id=7, name='100000', price=7, is_active=True)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d7), 'test 13.11')
        c1 = Customer(cust_id=1, full_name='1', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'test 13.12')
        c2 = Customer(cust_id=2, full_name='2', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2), 'test 13.13')
        c3 = Customer(cust_id=3, full_name='3', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c3), 'test 13.14')
        c4 = Customer(cust_id=4, full_name='4', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c4), 'test 13.15')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(1), 'test 13.16')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(2), 'test 13.17')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(3), 'test 13.18')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4),'test 13.19')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1,1,1), 'test 13.20')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(2,1,1), 'test 13.21')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1,1), 'test 13.22')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(2, 2, 2), 'test 13.23')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(2, 2), 'test 13.24')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(1), 'test 13.25')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(2), 'test 13.26')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(3), 'test 13.27')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4),'test 13.28')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(1, 1, 3), 'test 13.29')
        # d1's average rating = (1 + 3) / 2 = 2
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(1), 'test 13.30')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(2), 'test 13.31')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(3), 'test 13.32')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4), 'test 13.33')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(3, 1, 5), 'test 13.34')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(4, 1, 5), 'test 13.35')
        # d1's average rating = (1 + 3 + 5 + 5) / 4 = 3.5
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(1), 'test 13.36')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(2), 'test 13.37')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(3), 'test 13.38')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4), 'test 13.39')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(1, 2, 5), 'test 13.40')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(2, 2, 5), 'test 13.41')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(3, 2, 5), 'test 13.42')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(4, 2, 5), 'test 13.43')
        # d1's average rating = (1 + 3 + 5 + 5) / 4 = 3.5
        # d2's average rating = 5*4 / 4 = 5
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(3, 2, 2), 'test 13.44')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(3, 3), 'test 13.45')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(1), 'test 13.46')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(2), 'test 13.47')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(3), 'test 13.48')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4), 'test 13.49')
        c5 = Customer(cust_id=5, full_name='5', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c5), 'test 13.50')
        c6 = Customer(cust_id=6, full_name='6', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c6), 'test 13.51')
        c7 = Customer(cust_id=7, full_name='7', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c7), 'test 13.52')
        c8 = Customer(cust_id=8, full_name='8', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c8), 'test 13.53')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(5, 2, 1), 'test 13.54')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(6, 2, 1), 'test 13.55')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(7, 2, 1), 'test 13.56')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(8, 2, 1), 'test 13.57')
        # d2's average rating = (5*4 + 1*4) / 8 = 3
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(1), 'test 13.58')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(2), 'test 13.59')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(3), 'test 13.60')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4), 'test 13.61')
        c9 = Customer(cust_id=9, full_name='9', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c9), 'test 13.62')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(9, 2, 1), 'test 13.63')
        # d2's average rating = (5*4 + 1*5) / 9 = 2.777777778
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(1), 'test 13.64')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(2), 'test 13.65')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(3), 'test 13.66')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4), 'test 13.67')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(4, 4), 'test 13.68')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4), 'test 13.69')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(4, 2, 2), 'test 13.70')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4), 'test 13.71')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(4, 7, 1), 'test 13.72')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4), 'test 13.73')
        self.assertEqual(ReturnValue.OK,
                         Solution.order_contains_dish(4, 6, 1), 'test 13.74')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(4), 'test 13.75')
        self.assertEqual(ReturnValue.OK, Solution.customer_rated_dish(9, 6, 1), 'test 13.76')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(4), 'test 13.77')
        c10 = Customer(cust_id=10, full_name='10', age=22, phone="0123456789")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c10), 'test 13.78')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_rated_dish(10, 2, 5), 'test 13.79')
        # d2's average rating = (5*4 + 1*5 + 5) / 10 =3
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(4), 'test 13.80')
        self.assertEqual(ReturnValue.OK,
                         Solution.customer_deleted_rating_on_dish(10, 2), 'test 13.81')
        self.assertEqual(True, Solution.did_customer_order_top_rated_dishes(4), 'test 13.82')
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(4, 7), 'test 13.83')
        self.assertEqual(False, Solution.did_customer_order_top_rated_dishes(4), 'test 13.84')
        #
        # NOTE: MAKE MORE COMPREHENSIVE TESTS
        #


if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)

# If you fail any assert when running the
# tests all at once - try running them
# individually, as there is quite a lot
# going on here. Also, some tests are named
# after a single function, but actually
# test more than one.

# Test numbers (e.g. 'test 11.35') don't mean
# anything, they're just there to make it
# easy to know which assert failed, and
# they might not be in consecutive or
# correct order.