#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import commands, sys, time, locale

def main():
    locale.setlocale(locale.LC_ALL, "pt_BR.utf-8")

    for arg in sys.argv[1:]:
        
        time_st = time.time()

        print '\nArquivo:', arg

        status, output = commands.getstatusoutput('alpr -c eu --clock -n 5 %s' %arg) # retorna 2-tuple (status, output)

        if status:
            print 'Erro:', output
        else:
            result =  str(output).replace('    - ', '').replace('\t confidence:', '\t confiança:').split('\n')
            #print result
            #print 'Tempo total para processar a imagem:', result[0].split(': ')[1]

            if 'No license plates found.' in result[1]:
                print 'Nenhuma placa encontrada.'
            else:
                #print result[2:]
                for saida in result[2:]:
                    if len(saida.split('\t')[0]) == 7: # candidato válido
                        letras = saida.split('\t')[0][:3].replace('0', 'O').replace('1', 'I').replace('5', 'S').replace('6', 'G').replace('8', 'B')
                        num = saida.split('\t')[0][-4:].replace('O', '0').replace('I', '1').replace('S', '5').replace('G', '6').replace('B', '8').replace('D', '0')
                        print letras + '-' + num, saida[2:].split('\t')[1].replace('.', ',') # AAA-0000, confiança: 00,0000
                        
                        break
                    elif saida == result[2:][-1]: # última placa a analizar
                        print 'Nenhuma placa válida encontrada.'

        #print 'Tempo de execução:', "%.4f" %((time.time() - time_st)*1000) + 'ms'
        print 'Tempo de execução:', "{:n}".format((time.time() - time_st)*1000)

if __name__ == '__main__':
    main()