from datetime import date
class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        self.beneficios_usados = 0
    #Retorna a categoria do cliente. Na classe base, todo cliente é considerado "Comum".
    def obter_categoria(self):
        return "Comum"
    #Retorna o desconto do cliente comum, que é 0.0, ou seja, sem desconto.
    def obter_desconto(self):
        return 0.0
    #Retorna quantos benefícios o cliente pode usar. Cliente comum não possui benefícios, então retorna 0.
    def limite_beneficios(self):
        return 0
    #Calcula quantos benefícios o cliente ainda pode usar.
    def beneficios_restantes(self):
        return self.limite_beneficios() - self.beneficios_usados
    #Verifica se o cliente ainda tem benefícios disponíveis.
    def pode_usar_beneficio(self):
        return self.beneficios_restantes() > 0
    #Se o cliente tiver benefícios disponíveis, aumenta a quantidade de benefícios usados e retorna True.
    #Caso contrário, retorna False.
    def usar_beneficio(self):
        if self.pode_usar_beneficio():
            self.beneficios_usados += 1
            return True
        return False
#Retorna "Gold", Retorna 0.10, ou seja, cliente Gold tem 10% de desconto., 
#Retorna 1, ou seja, cliente Gold pode usar 1 benefício gratuito.
class ClienteGold(Cliente):
    def obter_categoria(self):
        return "Gold"
    def obter_desconto(self):
        return 0.10


    def limite_beneficios(self):
        return 1
#Retorna "Platinum"
#Retorna 0.15, ou seja, cliente Platinum tem 15% de desconto.
#Retorna 2, ou seja, cliente Platinum pode usar 2 benefícios gratuitos.
class ClientePlatinum(Cliente):
    def obter_categoria(self):
        return "Platinum"
    def obter_desconto(self):
        return 0.15
    def limite_beneficios(self):
        return 2
class Quarto:
    def __init__(self, numero, tipo, valor_diaria):
        self.numero = numero
        self.tipo = tipo
        self.valor_diaria = valor_diaria
#Cria uma reserva ligando os dados do cliente e define o status como "ativa" e já calcula o valor total da reserva.
class Reserva:
    def __init__(self, cliente, quarto, data_entrada, data_saida,
                 cafe=False, late_checkin=False, late_checkout=False):
        self.cliente = cliente
        self.quarto = quarto
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.cafe = cafe
        self.late_checkin = late_checkin
        self.late_checkout = late_checkout
        self.status = "ativa"
        self.beneficios_aplicados = []
        self.valor_total = self.calcular_valor()
    #Calcula a quantidade de diárias da reserva.
    def calcular_dias(self):
        return (self.data_saida - self.data_entrada).days
    #Verifica se a entrada ou a saída acontece em final de semana.
    def eh_final_de_semana(self):
        return self.data_entrada.weekday() >= 5 or self.data_saida.weekday() >= 5
    #Calcula o valor total da reserva.
    def calcular_valor(self):
        dias = self.calcular_dias()
        valor_base = self.quarto.valor_diaria * dias
        valor_cafe = 40 * dias if self.cafe else 0
        valor_late_checkin = 0
        valor_late_checkout = 0
        if self.late_checkin:
            if self.cliente.usar_beneficio():
                self.beneficios_aplicados.append("Late check-in gratuito")
            else:
                valor_late_checkin = 60
        if self.late_checkout:
            if self.cliente.usar_beneficio():
                self.beneficios_aplicados.append("Late check-out gratuito")
            else:
                valor_late_checkout = 80
        adicional_final_semana = 0
        if self.eh_final_de_semana():
            adicional_final_semana = valor_base * 0.10
        desconto = valor_base * self.cliente.obter_desconto()
        return valor_base + valor_cafe + valor_late_checkin + valor_late_checkout + adicional_final_semana - desconto
    #Altera o status da reserva para "cancelada".
    def cancelar(self):
        self.status = "cancelada"
    #Mostra na tela todos os dados da reserva, como cliente, CPF, categoria, quarto, datas, diárias, benefícios usados, status e valor total.
    def exibir_reserva(self):
        print("\n===== DADOS DA RESERVA =====")
        print("Cliente:", self.cliente.nome)
        print("CPF:", self.cliente.cpf)
        print("Categoria:", self.cliente.obter_categoria())
        print("Benefícios usados:", self.cliente.beneficios_usados)
        print("Benefícios restantes:", self.cliente.beneficios_restantes())
        print("Quarto:", self.quarto.numero, "-", self.quarto.tipo)
        print("Entrada:", self.data_entrada)
        print("Saída:", self.data_saida)
        print("Diárias:", self.calcular_dias())
        print("Café da manhã:", "Sim" if self.cafe else "Não")
        print("Late check-in:", "Sim" if self.late_checkin else "Não")
        print("Late check-out:", "Sim" if self.late_checkout else "Não")
        if len(self.beneficios_aplicados) > 0:
            print("Benefícios aplicados:")
            for beneficio in self.beneficios_aplicados:
                print("-", beneficio)
        else:
            print("Benefícios aplicados: Nenhum")
        print("Final de semana:", "Sim" if self.eh_final_de_semana() else "Não")
        print("Status:", self.status)
        print("Valor total: R$", round(self.valor_total, 2))
        print("-" * 40)
class Hotel:
    def __init__(self, nome):
        self.nome = nome
        self.clientes = []
        self.quartos = []
        self.reservas = []
    #Adiciona um cliente à lista de clientes do hotel.
    def cadastrar_cliente(self, cliente):
        self.clientes.append(cliente)
    #Adiciona um quarto à lista de quartos do hotel.
    def cadastrar_quarto(self, quarto):
        self.quartos.append(quarto)
    #Verifica se um quarto está disponível em determinado período.
    #Ela percorre as reservas ativas e verifica se existe conflito de datas.
    def quarto_disponivel(self, quarto, data_entrada, data_saida):
        for reserva in self.reservas:
            if reserva.quarto == quarto and reserva.status == "ativa":
                conflito = data_entrada < reserva.data_saida and data_saida > reserva.data_entrada
                if conflito:
                    return False
        return True
    #Cria uma reserva no hotel.
    def criar_reserva(self, cliente, quarto, data_entrada, data_saida,
                      cafe=False, late_checkin=False, late_checkout=False):
        if data_saida <= data_entrada:
            print("Erro: a data de saída deve ser maior que a data de entrada.")
            return None
        if not self.quarto_disponivel(quarto, data_entrada, data_saida):
            print("Erro: quarto indisponível para esse período.")
            return None
        reserva = Reserva(
            cliente,
            quarto,
            data_entrada,
            data_saida,
            cafe,
            late_checkin,
            late_checkout
        )
        self.reservas.append(reserva)
        print("Reserva criada com sucesso!")
        return reserva
    #Cancela uma reserva chamando o método cancelar() da própria reserva.
    def cancelar_reserva(self, reserva):
        reserva.cancelar()
        print("Reserva cancelada com sucesso!")
    #Mostra quais quartos estão disponíveis em um período.
    def consultar_disponibilidade(self, data_entrada, data_saida):
        print("\n===== QUARTOS DISPONÍVEIS =====")
        encontrou = False
        for quarto in self.quartos:
            if self.quarto_disponivel(quarto, data_entrada, data_saida):
                print("Quarto", quarto.numero, "-", quarto.tipo, "- R$", quarto.valor_diaria)
                encontrou = True
        if not encontrou:
            print("Nenhum quarto disponível nesse período.")
        print("-" * 40)
        print("\n===== RELATÓRIO DE LUCRO =====")
        reservas_ativas = []
        for reserva in self.reservas:
            if reserva.status == "ativa":
                reservas_ativas.append(reserva)
        if len(reservas_ativas) == 0:
            print("Nenhuma reserva ativa para análise.")
            return
        receita_total = 0
        reservas_com_cafe = 0
        reservas_final_semana = 0
        maior_valor = reservas_ativas[0]
        for reserva in reservas_ativas:
            receita_total += reserva.valor_total
            if reserva.cafe:
                reservas_com_cafe += 1
            if reserva.eh_final_de_semana():
                reservas_final_semana += 1
            if reserva.valor_total > maior_valor.valor_total:
                maior_valor = reserva
        media_receita = receita_total / len(reservas_ativas)
        print("Total de reservas ativas:", len(reservas_ativas))
        print("Receita total: R$", round(receita_total, 2))
        print("Média de receita por reserva: R$", round(media_receita, 2))
        print("Reservas com café da manhã:", reservas_com_cafe)
        print("Reservas em final de semana:", reservas_final_semana)
        print("Reserva mais lucrativa: quarto", maior_valor.quarto.numero, "-", maior_valor.cliente.nome)
        print("Valor da reserva mais lucrativa: R$", round(maior_valor.valor_total, 2))


        print("\nSugestões para maximizar o lucro:")
        if reservas_com_cafe < len(reservas_ativas):
            print("- Oferecer promoções de café da manhã para clientes que ainda não contrataram esse serviço.")
        if reservas_final_semana > 0:
            print("- Manter adicional em reservas de final de semana, pois são períodos de maior demanda.")
        if maior_valor.quarto.tipo.lower() in ["luxo", "premium", "suite", "suíte"]:
            print("- Priorizar pacotes promocionais para quartos de categoria superior.")
        print("- Avaliar descontos com cuidado para clientes Gold e Platinum, equilibrando fidelização e lucro.")
        print("- Incentivar late check-in e late check-out como serviços adicionais pagos quando o cliente não possuir benefícios.")
        print("-" * 40)
def ler_data(mensagem):
    print(mensagem)
    ano = int(input("Ano: "))
    mes = int(input("Mês: "))
    dia = int(input("Dia: "))
    return date(ano, mes, dia)
#CRIEI ESSA PARTE PARA USAR COMO TESTE==================
def cadastrar_cliente_console(hotel):
    print("\n===== CADASTRO DE CLIENTE =====")
    nome = input("Nome: ")
    cpf = input("CPF: ")
    print("\nCategoria do cliente:")
    print("1 - Comum")
    print("2 - Gold")
    print("3 - Platinum")
    opcao = input("Escolha: ")
    if opcao == "1":
        cliente = Cliente(nome, cpf)
    elif opcao == "2":
        cliente = ClienteGold(nome, cpf)
    elif opcao == "3":
        cliente = ClientePlatinum(nome, cpf)
    else:
        print("Categoria inválida. Cliente cadastrado como comum.")
        cliente = Cliente(nome, cpf)
    hotel.cadastrar_cliente(cliente)
    print("Cliente cadastrado com sucesso!")
def cadastrar_quarto_console(hotel):
    print("\n===== CADASTRO DE QUARTO =====")
    numero = int(input("Número do quarto: "))
    tipo = input("Tipo do quarto: ")
    valor_diaria = float(input("Valor da diária: "))
    quarto = Quarto(numero, tipo, valor_diaria)
    hotel.cadastrar_quarto(quarto)
    print("Quarto cadastrado com sucesso!")
def escolher_cliente(hotel):
    print("\n===== CLIENTES CADASTRADOS =====")
    for i, cliente in enumerate(hotel.clientes):
        print(i, "-", cliente.nome, "-", cliente.obter_categoria())
    indice = int(input("Escolha o número do cliente: "))
    return hotel.clientes[indice]
def escolher_quarto(hotel):
    print("\n===== QUARTOS CADASTRADOS =====")
    for i, quarto in enumerate(hotel.quartos):
        print(i, "-", quarto.numero, "-", quarto.tipo, "- R$", quarto.valor_diaria)
    indice = int(input("Escolha o número do quarto: "))
    return hotel.quartos[indice]
def criar_reserva_console(hotel):
    if len(hotel.clientes) == 0:
        print("Nenhum cliente cadastrado.")
        return
    if len(hotel.quartos) == 0:
        print("Nenhum quarto cadastrado.")
        return
    print("\n===== CRIAR RESERVA =====")
    cliente = escolher_cliente(hotel)
    quarto = escolher_quarto(hotel)
    data_entrada = ler_data("Data de entrada:")
    data_saida = ler_data("Data de saída:")
    cafe = input("Deseja café da manhã? (s/n): ").lower() == "s"
    late_checkin = input("Deseja late check-in? (s/n): ").lower() == "s"
    late_checkout = input("Deseja late check-out? (s/n): ").lower() == "s"




    reserva = hotel.criar_reserva(
        cliente,
        quarto,
        data_entrada,
        data_saida,
        cafe,
        late_checkin,
        late_checkout
    )
    if reserva:
        reserva.exibir_reserva()
def pausar():
    input("\nPressione ENTER para voltar ao menu...")
def consultar_disponibilidade_console(hotel):
    if len(hotel.quartos) == 0:
        print("\nNenhum quarto cadastrado.")
        pausar()
        return
    print("\n===== CONSULTAR DISPONIBILIDADE =====")
    data_entrada = ler_data("Data de entrada:")
    data_saida = ler_data("Data de saída:")
    hotel.consultar_disponibilidade(data_entrada, data_saida)
    pausar()


def listar_reservas(hotel):
    if len(hotel.reservas) == 0:
        print("\nNenhuma reserva cadastrada.")
        pausar()
        return
    print("\n===== TODAS AS RESERVAS =====")
    for i, reserva in enumerate(hotel.reservas):
        print("\nReserva número:", i)
        reserva.exibir_reserva()
    pausar()
def buscar_reservas_por_cliente(hotel):
    if len(hotel.reservas) == 0:
        print("\nNenhuma reserva cadastrada.")
        pausar()
        return
    nome = input("\nDigite o nome do cliente: ").lower()
    encontrou = False
    for reserva in hotel.reservas:
        if nome in reserva.cliente.nome.lower():
            reserva.exibir_reserva()
            encontrou = True
    if not encontrou:
        print("\nNenhuma reserva encontrada para esse cliente.")
    pausar()


def cancelar_reserva_console(hotel):
    if len(hotel.reservas) == 0:
        print("\nNenhuma reserva cadastrada.")
        pausar()
        return
    print("\n===== CANCELAR RESERVA =====")
    for i, reserva in enumerate(hotel.reservas):
        print(i, "-", reserva.cliente.nome, "-", reserva.quarto.numero, "-", reserva.status)
    indice = int(input("Digite o número da reserva que deseja cancelar: "))
    if indice >= 0 and indice < len(hotel.reservas):
        hotel.cancelar_reserva(hotel.reservas[indice])
    else:
        print("Número de reserva inválido.")
    pausar()
def menu():
    hotel = Hotel("Hotel Accord Exemplo")
    while True:
        print("\n===== MENU DO HOTEL =====")
        print("1 - Cadastrar cliente")
        print("2 - Cadastrar quarto")
        print("3 - Criar reserva")
        print("4 - Consultar disponibilidade")
        print("5 - Listar todas as reservas")
        print("6 - Buscar reserva por cliente")
        print("7 - Cancelar reserva")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            cadastrar_cliente_console(hotel)
        elif opcao == "2":
            cadastrar_quarto_console(hotel)
        elif opcao == "3":
            criar_reserva_console(hotel)
        elif opcao == "4":
            consultar_disponibilidade_console(hotel)
        elif opcao == "5":
            listar_reservas(hotel)
        elif opcao == "6":
            buscar_reservas_por_cliente(hotel)
        elif opcao == "7":
            cancelar_reserva_console(hotel)
        elif opcao == "0":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida.")
            pausar()
menu()
