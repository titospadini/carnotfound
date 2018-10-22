#-*- coding: utf-8 -*-
# =============================================================
#
#                       -- ROBOCAR --
#
# TIME: CarNotFound
# CARRO: 404
#
# =============================================================
#
# DESCRICAO: ControlHandler.py
# Python versao: 3
#
# Classe para manipular as imagens obtidas pela webcam com OpenCV.
#
# =============================================================

from CarHandler import CarHandler

objCarHandler = CarHandler()

class  ControlHandler():

        def decisao(self, Direcao, QtdeLinhas):

            if (QtdeLinhas == 0):
                print("PARE")
                objCarHandler.stop()
            else:
                objCarHandler.forward()
                if (Direcao > 0):
                    print("DIREITA")
                    objCarHandler.setAngle(115)
                if (Direcao < 0):
                    print("ESQUERDA")
                    objCarHandler.setAngle(75)
                if(Direcao == 0):
                    print("EM FRENTE")
                    objCarHandler.setAngle(90)
