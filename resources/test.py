from datetime import datetime

horariof = '31/05/2023 14:30'  # Exemplo de string de data e hora

horario = datetime.strptime(horariof, '%d/%m/%Y %H:%M')
horario_formatado = horario.strftime('%d/%m/%Y %H:%M')

print(horario_formatado)
