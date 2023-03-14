# Тестовое для разработчика

## Проблематика

1. На сайте codeforces есть [большая подборка задач](https://codeforces.com/problemset?order=BY_SOLVED_DESC) (ссылку приложил в формате отсортированности - это уже помощь вам в парсинге данных), мы учим учеников конкретным темам. На каждую тему есть десятки задач, но часто у одной задачи не одна, а сразу несколько тем.
2. Нужно написать парсер задач и их свойств:
    1. Темы (”математика”, “перебор”, “графы” …)
    2. Количество решений задач
    3. Название + номер
    4. Сложность задачи (800 / 900 …. и тд)
3. Сохранить их в БД и дополнять, в случае если этой задачи нет - то добавлять. Настроить парсинг страниц codeforces периодичностью 1 час

Теперь главный алгоритм:

1. Требуется для определенной сложности + тематики уметь получать подборку из 10 задач, которые преимущественно мы заранее распределим по контестам (набор задач)
2. Цель распределить так, чтобы не было пересечений, то есть выбрали мы тему сортировки - на нее выдается нам 10 задач, при этом они принадлежат только этому контесту (никакому более)

## **Как просматривать данные?**

1. Все это должно храниться в postgresql БД
2. Телеграмм бот с возможностью выбрать сложность + тему - и на нее отобразятся подборка задач
3. Поиск по задаче - выдать всю инфу, что мы знаем про задачу

В целом, это все уже реализовано школой… То есть задача реальная. И далее развиваемая. 

Это нужно в первую очередь для педагогов, которые готовят контесты для детей.