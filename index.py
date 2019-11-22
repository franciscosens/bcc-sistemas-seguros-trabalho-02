import numpy as np
import os
import binascii

s_box = [['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'],
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
         ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']]

matriz_l = [['0x00','0x00','0x19','0x01','0x32','0x02','0x1a','0xc6','0x4b','0xc7','0x1b','0x68','0x33','0xee','0xdf','0x03'], 
            ['0x64','0x04','0xe0','0x0e','0x34','0x8d','0x81','0xef','0x4c','0x71','0x08','0xc8','0xf8','0x69','0x1c','0xc1'], 
            ['0x7d','0xc2','0x1d','0xb5','0xf9','0xb9','0x27','0x6a','0x4d','0xe4','0xa6','0x72','0x9a','0xc9','0x09','0x78'], 
            ['0x65','0x2f','0x8a','0x05','0x21','0x0f','0xe1','0x24','0x12','0xf0','0x82','0x45','0x35','0x93','0xda','0x8e'], 
            ['0x96','0x8f','0xdb','0xbd','0x36','0xd0','0xce','0x94','0x13','0x5c','0xd2','0xf1','0x40','0x46','0x83','0x38'], 
            ['0x66','0xdd','0xfd','0x30','0xbf','0x06','0x8b','0x62','0xb3','0x25','0xe2','0x98','0x22','0x88','0x91','0x10'], 
            ['0x7e','0x6e','0x48','0xc3','0xa3','0xb6','0x1e','0x42','0x3a','0x6b','0x28','0x54','0xfa','0x85','0x3d','0xba'], 
            ['0x2b','0x79','0x0a','0x15','0x9b','0x9f','0x5e','0xca','0x4e','0xd4','0xac','0xe5','0xf3','0x73','0xa7','0x57'], 
            ['0xaf','0x58','0xa8','0x50','0xf4','0xea','0xd6','0x74','0x4f','0xae','0xe9','0xd5','0xe7','0xe6','0xad','0xe8'], 
            ['0x2c','0xd7','0x75','0x7a','0xeb','0x16','0x0b','0xf5','0x59','0xcb','0x5f','0xb0','0x9c','0xa9','0x51','0xa0'], 
            ['0x7f','0x0c','0xf6','0x6f','0x17','0xc4','0x49','0xec','0xd8','0x43','0x1f','0x2d','0xa4','0x76','0x7b','0xb7'], 
            ['0xcc','0xbb','0x3e','0x5a','0xfb','0x60','0xb1','0x86','0x3b','0x52','0xa1','0x6c','0xaa','0x55','0x29','0x9d'], 
            ['0x97','0xb2','0x87','0x90','0x61','0xbe','0xdc','0xfc','0xbc','0x95','0xcf','0xcd','0x37','0x3f','0x5b','0xd1'], 
            ['0x53','0x39','0x84','0x3c','0x41','0xa2','0x6d','0x47','0x14','0x2a','0x9e','0x5d','0x56','0xf2','0xd3','0xab'], 
            ['0x44','0x11','0x92','0xd9','0x23','0x20','0x2e','0x89','0xb4','0x7c','0xb8','0x26','0x77','0x99','0xe3','0xa5'], 
            ['0x67','0x4a','0xed','0xde','0xc5','0x31','0xfe','0x18','0x0d','0x63','0x8c','0x80','0xc0','0xf7','0x70','0x07']]

matriz_e = [['0x01', '0x03', '0x05', '0x0f', '0x11', '0x33', '0x55', '0xff', '0x1a', '0x2e', '0x72', '0x96', '0xa1', '0xf8', '0x13', '0x35'],
            ['0x5f', '0xe1', '0x38', '0x48', '0xd8', '0x73', '0x95', '0xa4', '0xf7', '0x02', '0x06', '0x0a', '0x1e', '0x22', '0x66', '0xaa'],
            ['0xe5', '0x34', '0x5c', '0xe4', '0x37', '0x59', '0xeb', '0x26', '0x6a', '0xbe', '0xd9', '0x70', '0x90', '0xab', '0xe6', '0x31'],
            ['0x53', '0xf5', '0x04', '0x0c', '0x14', '0x3c', '0x44', '0xcc', '0x4f', '0xd1', '0x68', '0xb8', '0xd3', '0x6e', '0xb2', '0xcd'],
            ['0x4c', '0xd4', '0x67', '0xa9', '0xe0', '0x3b', '0x4d', '0xd7', '0x62', '0xa6', '0xf1', '0x08', '0x18', '0x28', '0x78', '0x88'],
            ['0x83', '0x9e', '0xb9', '0xd0', '0x6b', '0xbd', '0xdc', '0x7f', '0x81', '0x98', '0xb3', '0xce', '0x49', '0xdb', '0x76', '0x9a'],
            ['0xb5', '0xc4', '0x57', '0xf9', '0x10', '0x30', '0x50', '0xf0', '0x0b', '0x1d', '0x27', '0x69', '0xbb', '0xd6', '0x61', '0xa3'],
            ['0xfe', '0x19', '0x2b', '0x7d', '0x87', '0x92', '0xad', '0xec', '0x2f', '0x71', '0x93', '0xae', '0xe9', '0x20', '0x60', '0xa0'],
            ['0xfb', '0x16', '0x3a', '0x4e', '0xd2', '0x6d', '0xb7', '0xc2', '0x5d', '0xe7', '0x32', '0x56', '0xfa', '0x15', '0x3f', '0x41'],
            ['0xc3', '0x5e', '0xe2', '0x3d', '0x47', '0xc9', '0x40', '0xc0', '0x5b', '0xed', '0x2c', '0x74', '0x9c', '0xbf', '0xda', '0x75'],
            ['0x9f', '0xba', '0xd5', '0x64', '0xac', '0xef', '0x2a', '0x7e', '0x82', '0x9d', '0xbc', '0xdf', '0x7a', '0x8e', '0x89', '0x80'],
            ['0x9b', '0xb6', '0xc1', '0x58', '0xe8', '0x23', '0x65', '0xaf', '0xea', '0x25', '0x6f', '0xb1', '0xc8', '0x43', '0xc5', '0x54'],
            ['0xfc', '0x1f', '0x21', '0x63', '0xa5', '0xf4', '0x07', '0x09', '0x1b', '0x2d', '0x77', '0x99', '0xb0', '0xcb', '0x46', '0xca'],
            ['0x45', '0xcf', '0x4a', '0xde', '0x79', '0x8b', '0x86', '0x91', '0xa8', '0xe3', '0x3e', '0x42', '0xc6', '0x51', '0xf3', '0x0e'],
            ['0x12', '0x36', '0x5a', '0xee', '0x29', '0x7b', '0x8d', '0x8c', '0x8f', '0x8a', '0x85', '0x94', '0xa7', '0xf2', '0x0d', '0x17'],
            ['0x39', '0x4b', '0xdd', '0x7c', '0x84', '0x97', '0xa2', '0xfd', '0x1c', '0x24', '0x6c', '0xb4', '0xc7', '0x52', '0xf6', '0x01']]

matriz_expansao_chaves = []

def compensar_inteiro(valor):
    if len(valor) == 4:
        return valor
        
    valor = valor.replace("0x", "")
    return "0x0" + valor

def converter_hexa_int(valor):
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

def descobrir_valor_s_box(posicao):
    posicao = posicao.replace('0x', '')
    linha = converter_hexa_int(posicao[0].upper())
    coluna = converter_hexa_int(posicao[1].upper())
    return '0x' + s_box[linha][coluna]

def gerar_chaves(round_key):
    round_key_anterior = round_key - 1
    round_key_anterior_outro_bloco = round_key_anterior - 3
    matriz_expansao_chaves[0][round_key] = compensar_inteiro(hex(int(matriz_expansao_chaves[0][round_key_anterior], 0) ^ int(matriz_expansao_chaves[0][round_key_anterior_outro_bloco], 0)))
    matriz_expansao_chaves[1][round_key] = compensar_inteiro(hex(int(matriz_expansao_chaves[1][round_key_anterior], 0) ^ int(matriz_expansao_chaves[1][round_key_anterior_outro_bloco], 0)))
    matriz_expansao_chaves[2][round_key] = compensar_inteiro(hex(int(matriz_expansao_chaves[2][round_key_anterior], 0) ^ int(matriz_expansao_chaves[2][round_key_anterior_outro_bloco], 0)))
    matriz_expansao_chaves[3][round_key] = compensar_inteiro(hex(int(matriz_expansao_chaves[3][round_key_anterior], 0) ^ int(matriz_expansao_chaves[3][round_key_anterior_outro_bloco], 0)))

def rotacionar_bytes(round_key):
    round_posicao = round_key * 4
    round_anterior_posicao = (round_key - 1) * 4

    vetor_round_constants  = ['0x01','0x02','0x04','0x08','0x10','0x20','0x40','0x80','0x1B', '0x36']
    round_constant = [vetor_round_constants[round_key - 1], '0x00', '0x00', '0x00']

    valorPosicao0 = matriz_expansao_chaves[0][round_posicao - 1]
    valorPosicao1 = matriz_expansao_chaves[1][round_posicao - 1]
    valorPosicao2 = matriz_expansao_chaves[2][round_posicao - 1]
    valorPosicao3 = matriz_expansao_chaves[3][round_posicao - 1]

    valorRoundKeyAnteriorPosicao0 = matriz_expansao_chaves[0][round_anterior_posicao]
    valorRoundKeyAnteriorPosicao1 = matriz_expansao_chaves[1][round_anterior_posicao]
    valorRoundKeyAnteriorPosicao2 = matriz_expansao_chaves[2][round_anterior_posicao]
    valorRoundKeyAnteriorPosicao3 = matriz_expansao_chaves[3][round_anterior_posicao]

    valorSBox0 = descobrir_valor_s_box(valorPosicao1)
    valorSBox1 = descobrir_valor_s_box(valorPosicao2)
    valorSBox2 = descobrir_valor_s_box(valorPosicao3)
    valorSBox3 = descobrir_valor_s_box(valorPosicao0)

    valorXorRoundKey0 = hex(int(valorSBox0, 0) ^ int(round_constant[0], 0))
    valorXorRoundKey1 = hex(int(valorSBox1, 0) ^ int(round_constant[1], 0))
    valorXorRoundKey2 = hex(int(valorSBox2, 0) ^ int(round_constant[2], 0))
    valorXorRoundKey3 = hex(int(valorSBox3, 0) ^ int(round_constant[3], 0))

    valorXorRoundKeyComRoundKeyAnterior0 = hex(int(valorXorRoundKey0, 0) ^ (int(valorRoundKeyAnteriorPosicao0, 0)))
    valorXorRoundKeyComRoundKeyAnterior1 = hex(int(valorXorRoundKey1, 0) ^ (int(valorRoundKeyAnteriorPosicao1, 0)))
    valorXorRoundKeyComRoundKeyAnterior2 = hex(int(valorXorRoundKey2, 0) ^ (int(valorRoundKeyAnteriorPosicao2, 0)))
    valorXorRoundKeyComRoundKeyAnterior3 = hex(int(valorXorRoundKey3, 0) ^ (int(valorRoundKeyAnteriorPosicao3, 0)))

    matriz_expansao_chaves[0][round_posicao] = valorXorRoundKeyComRoundKeyAnterior0
    matriz_expansao_chaves[1][round_posicao] = valorXorRoundKeyComRoundKeyAnterior1
    matriz_expansao_chaves[2][round_posicao] = valorXorRoundKeyComRoundKeyAnterior2
    matriz_expansao_chaves[3][round_posicao] = valorXorRoundKeyComRoundKeyAnterior3

def retornar_round_key(round):
    if (round >= 1):
        round = round * 4
    
    matriz_retorno = []

    for linha in range(4):
        matriz_retorno.append(['']*4)
    
    for linha in range(4):
        matriz_retorno[linha][0] = matriz_expansao_chaves[linha][round] 
        matriz_retorno[linha][1] = matriz_expansao_chaves[linha][round + 1]
        matriz_retorno[linha][2] = matriz_expansao_chaves[linha][round + 2]
        matriz_retorno[linha][3] = matriz_expansao_chaves[linha][round + 3]

    return matriz_retorno

def expansao_chave(chave):
    chave = chave.split(', ')
    posicao_linha = 0
    
    for linha in range(4):
        matriz_expansao_chaves.append(['']*44)

    for coluna in range(4):
        for linha in range(4):
            matriz_expansao_chaves[linha][coluna] =chave[posicao_linha]
            posicao_linha = posicao_linha + 1

    for i in range(1, 11):
        rotacionar_bytes(i)
        posicao = i * 4

        gerar_chaves(posicao + 1)
        gerar_chaves(posicao + 2)
        gerar_chaves(posicao + 3)

# PKCS#5
def retornar_texto_primeiro_bloco(texto):
    valor_bloco = 8 - len(texto.split(' '))

    for i in range(valor_bloco):
        texto = texto + ' ' + hex(valor_bloco)
        
    return texto

# PKCS#5
def retornar_texto_segundo_bloco(texto):
    valor_subtracao = 16 - len(texto.split(' '))
        
    for i in range(valor_subtracao):
        texto = texto + ' ' + hex(valor_subtracao)
        
    return texto

# PKCS#5
def corrigir_tamanho_texto_simples(texto_simples):
    tamanho_texto = len(texto_simples.split(' '))
    
    if (tamanho_texto < 16):
        novo_texto_simples = ''
        
        if ((16 - tamanho_texto) > 8):
            novo_texto_simples = retornar_texto_primeiro_bloco(texto_simples)
            novo_texto_simples = retornar_texto_segundo_bloco(novo_texto_simples)
        else:
            novo_texto_simples = retornar_texto_segundo_bloco(texto_simples)
        
        return novo_texto_simples.split(' ')
    
    return texto_simples.split(' ')

def transformar_texto_em_matriz(texto_simples):
    matriz_retorno = []
    posicao_linha = 0

    for linha in range(4):
        matriz_retorno.append(['']*4)
        
    for coluna in range(4):
        for linha in range(4):
            matriz_retorno[linha][coluna] = texto_simples[posicao_linha]
            posicao_linha += 1
        
    return matriz_retorno

# Primeira etapa da cifragem - XOR entre o texto simples com a round key da rodada
def converter_matriz_hex_para_int(matriz):
    matriz_retorno = np.arange(1, 17).reshape(4, 4)

    for linha in range(4):
        for coluna in range(4):
            matriz_retorno[linha][coluna] = int(matriz[linha][coluna], 0)
        
    return matriz_retorno
    
def realizar_xor_entre_matrizes(matriz_texto_simples, round_key_rodada):
    valor_xor = np.bitwise_xor(converter_matriz_hex_para_int(matriz_texto_simples), converter_matriz_hex_para_int(round_key_rodada))
    
    converter_hex = np.vectorize(hex)
    return converter_hex(valor_xor) 

# Segunda etapa da cifragem - Alterar os valores obtidos na primeira etapa com os valores da SBox
def substituir_valores_matriz_com_sBox(matriz_primeira_etapa):
    for linha in range(4):
        for coluna in range(4):
            valor_substituicao = matriz_primeira_etapa[linha][coluna][2:].zfill(2)
            matriz_primeira_etapa[linha][coluna] = descobrir_valor_s_box(valor_substituicao)
        
    return matriz_primeira_etapa

# Terceira etapa da cifragem - Alterar a posição dos valores na matriz resultante da segunda etapa
def realizar_shiftRows(matriz_segunda_etapa):
    matriz_retorno = []
    
    for i in range(4):
        matriz_retorno.append(['']*4)
    
    matriz_retorno[0][0] = matriz_segunda_etapa[0][0]
    matriz_retorno[0][1] = matriz_segunda_etapa[0][1]
    matriz_retorno[0][2] = matriz_segunda_etapa[0][2]
    matriz_retorno[0][3] = matriz_segunda_etapa[0][3]
    
    matriz_retorno[1][0] = matriz_segunda_etapa[1][1]
    matriz_retorno[1][1] = matriz_segunda_etapa[1][2]
    matriz_retorno[1][2] = matriz_segunda_etapa[1][3]
    matriz_retorno[1][3] = matriz_segunda_etapa[1][0]
    
    matriz_retorno[2][0] = matriz_segunda_etapa[2][2]
    matriz_retorno[2][1] = matriz_segunda_etapa[2][3]
    matriz_retorno[2][2] = matriz_segunda_etapa[2][0]
    matriz_retorno[2][3] = matriz_segunda_etapa[2][1]
    
    matriz_retorno[3][0] = matriz_segunda_etapa[3][3]
    matriz_retorno[3][1] = matriz_segunda_etapa[3][0]
    matriz_retorno[3][2] = matriz_segunda_etapa[3][1]
    matriz_retorno[3][3] = matriz_segunda_etapa[3][2]

    return matriz_retorno

def obter_valor_galeos(primeiro_valor, segundo_valor):
    if (primeiro_valor == '0x00' or segundo_valor == '0x00'):
        return '0x00'
    
    if (primeiro_valor == '0x01'):
        return segundo_valor
    
    if (segundo_valor == '0x01'):
        return primeiro_valor
    
    posicao_primeiro_valor = primeiro_valor.replace('0x', '')
    linha_primeiro_valor = converter_hexa_int(posicao_primeiro_valor[0].upper())
    coluna_primeiro_valor = converter_hexa_int(posicao_primeiro_valor[1].upper())
    primeiro_valor_matriz_galeos = matriz_l[linha_primeiro_valor][coluna_primeiro_valor]
    
    posicao_segundo_valor = segundo_valor.replace('0x', '')
    linha_segundo_valor = converter_hexa_int(posicao_segundo_valor[0].upper())
    coluna_segundo_valor = converter_hexa_int(posicao_segundo_valor[1].upper())
    segundo_valor_matriz_galeos = matriz_l[linha_segundo_valor][coluna_segundo_valor] 
    
    resultado = int(primeiro_valor_matriz_galeos, 0) + int(segundo_valor_matriz_galeos, 0)
    if (resultado > 255):
        resultado = resultado - 255
        
    resultado = hex(resultado)[2:].zfill(2)
    posicao_linha_resultado = resultado.replace('0x', '')
    linha_resultado = converter_hexa_int(posicao_linha_resultado[0].upper())
    coluna_resultado = converter_hexa_int(posicao_linha_resultado[1].upper())
    
    return matriz_e[linha_resultado][coluna_resultado]

# Quarta etapa da cifragem - Realizar o mixColumns
def realizar_mixColumns(matriz_terceira_etapa):
    matriz_multiplicacao = [['0x02', '0x03', '0x01', '0x01'],
                            ['0x01', '0x02', '0x03', '0x01'],
                            ['0x01', '0x01', '0x02', '0x03'],
                            ['0x03', '0x01', '0x01', '0x02']]
    matriz_retorno = np.arange(1, 17).reshape(4, 4)
    
    for i in range(len(matriz_terceira_etapa)):
        for j in range(len(matriz_terceira_etapa[i])):
            valores_matriz_multiplicacao = matriz_multiplicacao[j]
            valores = matriz_terceira_etapa[j]

            r1 = matriz_terceira_etapa[0][i]
            r2 = matriz_terceira_etapa[1][i]
            r3 = matriz_terceira_etapa[2][i]
            r4 = matriz_terceira_etapa[3][i]

            valor_multiplicacao_1 = valores_matriz_multiplicacao[0]
            valor_multiplicacao_2 = valores_matriz_multiplicacao[1]
            valor_multiplicacao_3 = valores_matriz_multiplicacao[2]
            valor_multiplicacao_4 = valores_matriz_multiplicacao[3]

            resultado_multiplicacao_1 = obter_valor_galeos(r1, valor_multiplicacao_1)
            resultado_multiplicacao_2 = obter_valor_galeos(r2, valor_multiplicacao_2)
            resultado_multiplicacao_3 = obter_valor_galeos(r3, valor_multiplicacao_3)
            resultado_multiplicacao_4 = obter_valor_galeos(r4, valor_multiplicacao_4)

            primeiro_valor_xor = np.bitwise_xor(int(resultado_multiplicacao_1, 0), int(resultado_multiplicacao_2, 0))
            segundo_valor_xor = np.bitwise_xor(primeiro_valor_xor, int(resultado_multiplicacao_3, 0))
            terceiro_valor_xor = np.bitwise_xor(segundo_valor_xor, int(resultado_multiplicacao_4, 0))
            matriz_retorno[j][i] = terceiro_valor_xor
    
    converter_hex = np.vectorize(hex)
    return converter_hex(matriz_retorno) 

# Quinta etapa da cifragem - Xor entre a matriz resultante do mixColumns com a round key da rodada
def realizar_add_round_key(matriz_quarta_etapa, round_key_rodada):
    valor_xor = np.bitwise_xor(converter_matriz_hex_para_int(matriz_quarta_etapa), converter_matriz_hex_para_int(round_key_rodada))
    
    converter_hex = np.vectorize(hex)
    return converter_hex(valor_xor) 

def salvar_texto_cifrado(texto_cifrado):
    arquivo = open('TextoCifrado.txt', 'w')
    arquivo.write('*** Texto cifrado ***')
    arquivo.write('\n')
    arquivo.write(str(texto_cifrado))
    arquivo.close()


def cifrar(texto_simples):
    texto_simples_corrigido = corrigir_tamanho_texto_simples(texto_simples.strip())
    matriz_texto_simples = transformar_texto_em_matriz(texto_simples_corrigido)
    
    round_key = retornar_round_key(0)
    matriz_quinta_etapa = []
    
    for i in range(1, 11):
        
        if (matriz_quinta_etapa == []):
            # Matriz primeira etapa
            matriz_primeira_etapa = realizar_xor_entre_matrizes(matriz_texto_simples, round_key)

            # Matriz segunda etapa
            matriz_segunda_etapa = substituir_valores_matriz_com_sBox(matriz_primeira_etapa)
        else:
            # Matriz segunda etapa
            matriz_segunda_etapa = substituir_valores_matriz_com_sBox(matriz_quinta_etapa)

        # Matriz terceira etapa
        matriz_terceira_etapa = realizar_shiftRows(matriz_segunda_etapa)

        if (i != 10):
            # Matriz quarta etapa
            matriz_quarta_etapa = realizar_mixColumns(matriz_terceira_etapa)
        else:
            matriz_quarta_etapa = matriz_terceira_etapa
            
        round_key = retornar_round_key(i)
            
        # Matriz quinta etapa
        matriz_quinta_etapa = realizar_add_round_key(matriz_quarta_etapa, round_key)
        
    salvar_texto_cifrado(matriz_quinta_etapa)


def cifrar_texto_string(texto_simples_string):
    texto = texto_simples_string.encode('utf-8') 
    texto_hex = texto.hex()
    texto_retorno = ''

    for i in range(0, len(texto_hex), 2):
        texto_retorno += ('0x' + texto_hex[i] + texto_hex[i+1] + ' ')
    
    cifrar(texto_retorno)

arquivo_ser_cifrado = 'assets/imagem.jpg'
texto_simples = open(arquivo_ser_cifrado, 'r').read()

arquivo_gerado = 'assets/chave.txt'
chave = open(arquivo_gerado, 'r').read()

expansao_chave(chave)
cifrar_texto_string('DESENVOLVIMENTO')

