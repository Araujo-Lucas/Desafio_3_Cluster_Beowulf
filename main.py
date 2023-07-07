import subprocess
import sys

def verificar_igualdade(saida, saida2):
    """ 
    Método responsável por fazer a verificação da sincronização do nome do arquivo, seus dados e valores hash. Caso a sincronização não for confirmada a função retorna uma mensagem de aviso. Se for confirmada, retorna o resultado da funcionalidade
    """
    arquivos1 = saida.decode('utf-8').split()
    arquivos2 = saida2.decode('utf-8').split()

    arquivos_iguais = []
    resultado = ""

    for arquivo1 in arquivos1:
        if arquivo1 in arquivos2:
            comando_stat1 = f'ssh node1 stat -c "%s,%Y" {arquivo1}'
            info_arquivo1 = subprocess.check_output(comando_stat1, shell=True, text=True).strip().split(',')

            comando_stat2 = f'ssh node2 stat -c "%s,%Y" {arquivo1}'
            info_arquivo2 = subprocess.check_output(comando_stat2, shell=True, text=True).strip().split(',')

            if info_arquivo1[0] == info_arquivo2[0] and info_arquivo1[1] == info_arquivo2[1]:
                comando_md5_1 = f'ssh node1 md5sum {arquivo1}'
                hash_arquivo1 = subprocess.check_output(comando_md5_1, shell=True, text=True).strip().split()[0]

                comando_md5_2 = f'ssh node2 md5sum {arquivo1}'
                hash_arquivo2 = subprocess.check_output(comando_md5_2, shell=True, text=True).strip().split()[0]

                if hash_arquivo1 == hash_arquivo2:
                    arquivos_iguais.append(arquivo1)
                    resultado = True
                else:
                    resultado = False
                    break
    if resultado:
        for arquivo in arquivos_iguais:
            print(arquivo)
    else:
        print("Os arquivos não estão síncronos")

def copiar_arquivo(origem, destino):
    """
    Método responsável por copiar um arquivo de um local de origem para um local de destino em ambas as máquinas virtuais
    """
    subprocess.check_output(f'ssh node1 cp {origem} {destino}', shell=True)
    subprocess.check_output(f'ssh node2 cp {origem} {destino}', shell=True)

def copiar_diretorio(origem, destino):
    """
    Método responsável por copiar um diretório de um local de origem para um local de destino em ambas as máquinas virtuais
    """
    subprocess.check_output(f'ssh node1 cp -r {origem} {destino}', shell=True)
    subprocess.check_output(f'ssh node2 cp -r {origem} {destino}', shell=True)

def renomear_mover_arquivo(nome_atual, novo_nome):
    """
    Método responsável por renomear e/ou mover um arquivo. Caso o usuário apenas deseje renomear o arquivo, só é preciso informar o nome atual e o novo nome desejado para o arquivo. Se quiser também executar a funcionalidade de mover o arquivo, o usuário deve incluir o caminho de destino do arquivo junto com o novo nome ou com o mesmo nome anterior.
    """
    subprocess.check_output(f'ssh node1 "mv {nome_atual} {novo_nome}"', shell=True)
    subprocess.check_output(f'ssh node2 "mv {nome_atual} {novo_nome}"', shell=True)

def deletar_arquivo(arquivo):
    """
    Método responsável por deletar um arquivo em ambas as máquinas virtuais.
    """
    subprocess.check_output(f'ssh node1 rm {arquivo}', shell=True)
    subprocess.check_output(f'ssh node2 rm {arquivo}', shell=True)

def deletar_diretorio(diretorio):
    """
    Método responsável por deletar um diretório em ambas as máquinas virtuais.
    """
    subprocess.check_output(f'ssh node1 rm -r {diretorio}', shell=True)
    subprocess.check_output(f'ssh node2 rm -r {diretorio}', shell=True)

argumentos = sys.argv
comando = argumentos[1]
if comando == "ls":
    saida = subprocess.check_output('ssh node1 ls', shell=True)
    saida2 = subprocess.check_output('ssh node2 ls', shell=True)
    verificar_igualdade(saida, saida2)

elif comando == "rm":
    if len(argumentos) == 3:
        arquivo = argumentos[2]
        deletar_arquivo(arquivo)
    else:
        diretorio = argumentos[3]
        deletar_diretorio(diretorio)

elif comando == "cp":
    if len(argumentos) == 5:
        origem = argumentos[3]
        destino = argumentos[4]
        copiar_diretorio(origem, destino)
    else:
        origem = argumentos[2]
        destino = argumentos[3]
        copiar_arquivo(origem, destino)

elif comando == "mv":
    nome_atual = argumentos[2]
    novo_nome = argumentos[3]
    renomear_mover_arquivo(nome_atual, novo_nome)
else:
    print("Comando inválido")

