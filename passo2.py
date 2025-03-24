import time
from plyer import notification

def notificacao(intervalo_minutos=1):
    while True:
        notification.notify(
            title = 'Relatorio',
            message = "O produto mais vendido foi o café com 703",
            timeout = 10

        )
        time.sleep(intervalo_minutos*40)
notificacao()
    




    