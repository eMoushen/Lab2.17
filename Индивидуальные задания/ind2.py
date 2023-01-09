#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import json
import os


def add_prod(products, name, price, shope):
    """
    Добавить данные о товаре.
    """
    products.append(
        {
            "name": name,
            "price": price,
            "shope": shope,
        }
    )
    return products


def show_list(products):
    """
    Вывести список товаров
    """
    if products:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 5,
            '-' * 20,
            '-' * 14,
            '-' * 17
        )
        print(line)
        print(
            '| {:^5} | {:^20} | {:^14} | {:^17} |'.format(
                "№",
                "Название товара",
                "Цена",
                "Название магазина"
            )
        )
        print(line)

        # Вывести данные о всех товарах.
        for idx, product in enumerate(products, 1):
            print(
                '| {:>5} | {:<20} | {:<14.2f} | {:>17} |'.format(
                    idx,
                    product.get('name', ''),
                    product.get('price', 0),
                    product.get('shope', '')
                )
            )
        print(line)
    else:
        print("Список товаров пуст.")


def show_selected(products, name):
    """
    Проверить наличие товара
    """
    # Сформировать список товаров.
    result = [product for product in products if name == product.get('name', '')]

    # Возвратить список выбранных товаров.
    return result


def save_products(file_name, products):
    """
    Сохранение товаров
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(products, fout, ensure_ascii=False, indent=4)


def load_products(file_name):
    """
    Загрузить товары
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


@click.command()
@click.argument('filename')
@click.option('--command', '-c', help="Commands")
@click.option('--name', '-n', help="The product's name")
@click.option('--price', '-p', type=float, help="The product's price")
@click.option('--shope', '-s', help="The product's shope")
def main(filename, command, name, price, shope):
    """
    Главная функция программы.
    """
    # Загрузить всех студентов из файла, если файл существует.
    is_dirty = False
    if os.path.exists(filename):
        products = load_products(filename)
    else:
        products = []

    # Добавить товар.
    if command == "add":
        products = add_prod(products, name, price, shope)
        is_dirty = True

    # Отобразить все товары.
    elif command == "display":
        show_list(products)

    # Выбрать требуемый товар.
    elif command == "select":
        selected = show_selected(products, name)
        show_list(selected)

    # Сохранить данные в файл, если список товаров был изменен.
    if is_dirty:
        save_products(filename, products)


if __name__ == '__main__':
    main()
