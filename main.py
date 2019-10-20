import os 

class CifraAES:

    def __init__(self, texto, chave):
        self.texto = texto
        self.chave = chave.split(', ')
        self.matriz = []
        self.expansao_chave()

    def expansao_chave(self):
        posicao_linha = 0
        for linha in range(4):
            self.matriz.append(['']*44)

        for coluna in range(4):
            for linha in range(4):
                self.matriz[linha][coluna] = self.chave[posicao_linha]
                posicao_linha = posicao_linha + 1

        self.print_round(0)
        for i in range(1, 11):
            self.rotacionar_bytes(i)
            posicao = i * 4

            self.gerar_chaves(posicao + 1)
            self.gerar_chaves(posicao + 2)
            self.gerar_chaves(posicao + 3)
            self.print_round(i)
        
    def rotacionar_bytes(self, round_key):
        round_posicao = round_key * 4
        round_anterior_posicao = (round_key - 1) * 4

        vetor_round_constants  = ['0x01','0x02','0x04','0x08','0x10','0x20','0x40','0x80','0x1B', '0x36']
        round_constant = [vetor_round_constants[round_key - 1], '0x00', '0x00', '0x00']

        valorPosicao0 = self.matriz[0][round_posicao - 1]
        valorPosicao1 = self.matriz[1][round_posicao - 1]
        valorPosicao2 = self.matriz[2][round_posicao - 1]
        valorPosicao3 = self.matriz[3][round_posicao - 1]

        valorRoundKeyAnteriorPosicao0 = self.matriz[0][round_anterior_posicao]
        valorRoundKeyAnteriorPosicao1 = self.matriz[1][round_anterior_posicao]
        valorRoundKeyAnteriorPosicao2 = self.matriz[2][round_anterior_posicao]
        valorRoundKeyAnteriorPosicao3 = self.matriz[3][round_anterior_posicao]

        valorSBox0 = self.descobrir_valor_s_box(valorPosicao1)
        valorSBox1 = self.descobrir_valor_s_box(valorPosicao2)
        valorSBox2 = self.descobrir_valor_s_box(valorPosicao3)
        valorSBox3 = self.descobrir_valor_s_box(valorPosicao0)

        valorXorRoundKey0 = hex(int(valorSBox0, 0) ^ int(round_constant[0], 0))
        valorXorRoundKey1 = hex(int(valorSBox1, 0) ^ int(round_constant[1], 0))
        valorXorRoundKey2 = hex(int(valorSBox2, 0) ^ int(round_constant[2], 0))
        valorXorRoundKey3 = hex(int(valorSBox3, 0) ^ int(round_constant[3], 0))

        valorXorRoundKeyComRoundKeyAnterior0 = hex(int(valorXorRoundKey0, 0) ^ (int(valorRoundKeyAnteriorPosicao0, 0)))
        valorXorRoundKeyComRoundKeyAnterior1 = hex(int(valorXorRoundKey1, 0) ^ (int(valorRoundKeyAnteriorPosicao1, 0)))
        valorXorRoundKeyComRoundKeyAnterior2 = hex(int(valorXorRoundKey2, 0) ^ (int(valorRoundKeyAnteriorPosicao2, 0)))
        valorXorRoundKeyComRoundKeyAnterior3 = hex(int(valorXorRoundKey3, 0) ^ (int(valorRoundKeyAnteriorPosicao3, 0)))

        self.matriz[0][round_posicao] = valorXorRoundKeyComRoundKeyAnterior0
        self.matriz[1][round_posicao] = valorXorRoundKeyComRoundKeyAnterior1
        self.matriz[2][round_posicao] = valorXorRoundKeyComRoundKeyAnterior2
        self.matriz[3][round_posicao] = valorXorRoundKeyComRoundKeyAnterior3
        
    def gerar_chaves(self, round_key):
        round_key_anterior = round_key - 1
        round_key_anterior_outro_bloco = round_key_anterior - 3
        self.matriz[0][round_key] = self.compensar_inteiro(hex(int(self.matriz[0][round_key_anterior], 0) ^ int(self.matriz[0][round_key_anterior_outro_bloco], 0)))
        self.matriz[1][round_key] = self.compensar_inteiro(hex(int(self.matriz[1][round_key_anterior], 0) ^ int(self.matriz[1][round_key_anterior_outro_bloco], 0)))
        self.matriz[2][round_key] = self.compensar_inteiro(hex(int(self.matriz[2][round_key_anterior], 0) ^ int(self.matriz[2][round_key_anterior_outro_bloco], 0)))
        self.matriz[3][round_key] = self.compensar_inteiro(hex(int(self.matriz[3][round_key_anterior], 0) ^ int(self.matriz[3][round_key_anterior_outro_bloco], 0)))
    
    def compensar_inteiro(self, valor):
        if len(valor) == 4:
            return valor
        
        valor = valor.replace("0x", "")
        return "0x0" + valor

    def print_round(self, round):
        print(f'****RoundKey={round}****')
        if(round >= 1):
            round = round * 4
        for linha in range(4):
            print(self.matriz[linha][round], self.matriz[linha][round + 1], self.matriz[linha][round + 2], self.matriz[linha][round + 3])
        print()
 
    def converter_hexa_int(self, valor):
        if(valor == 'A'):
            return 10
        elif(valor == 'B'):
            return 11
        elif(valor == 'C'):
            return 12
        elif(valor == 'D'):
            return 13
        elif(valor == 'E'):
            return 14
        elif(valor == 'F'):
            return 15
        return int(valor)

    def descobrir_valor_s_box(self, posicao):
        posicao = posicao.replace('0x', '')
        posicao_linha = posicao[0].upper()
        posicao_coluna = posicao[1].upper()
        linha = self.converter_hexa_int(posicao_linha)
        coluna = self.converter_hexa_int(posicao_coluna)
        s_box = [
            ['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'],
            ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'],
            ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'],
            ['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'],
            ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],
            ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'],
            ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'],
            ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'],
            ['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'],
            ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'],
            ['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'],
            ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'],
            ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'],
            ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'],
            ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'],
            ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16'],
        ]
        return '0x' + s_box[linha][coluna]

    def cifragem_bloco(self):
        pass


if __name__ == "__main__":

    # arquivo_ser_cifrado = input('Digite o nome do arquivo a ser cifrado')
    arquivo_ser_cifrado = 'assets/arquivo_a_ser_cifrado.txt'
    texto = open(arquivo_ser_cifrado, 'r').read()
    
    
    # arquivo_gerado = input('Digite o nome do arquivo de destino')

    # Apagar esta parte, somente para facilitar
    arquivo_gerado = 'assets/chave.txt'
    chave = open(arquivo_gerado, 'r').read()

    # matriz_estado = 
    cifra = CifraAES(texto, chave)


