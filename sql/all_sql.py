"""
Здесь содержатся все запросы sql
"""

#  Тип данных столбца tg в базе данных — это строка, не пердавать в запросе значение в виде целого числа !
get_tg_id_jar = """SELECT code as user_id FROM inlet.staff_for_bot WHERE tg = '{0}'"""


get_user_data_gp_mart_sv = """
SELECT
    emp_type as role, emp_guid as guid 
FROM 
    mart_sv.employees_position_for_bot 
WHERE
    emp_code_1c = '{0}'
"""


# bot_table.tg in ({0})