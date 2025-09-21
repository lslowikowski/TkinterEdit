import AppController
class TkinterEdit:
    '''Klasa uruchomieniowa'''
    def __init__(self):
        '''Uruchamiamy appControler,
        który jest sercem aplikacji
        zarządza i komunikuje się z pozostałymi klasami'''
        self.appControler = AppController.AppController()

if __name__ == '__main__':
    '''uruchomienie instancji klasy TkinterEdit'''
    tkinterEdit = TkinterEdit()