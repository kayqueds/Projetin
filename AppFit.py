import mysql.connector

# Conexão com o banco de dados MySQL
cnn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="AppFit"
)
cursor = cnn.cursor()

# Login do usuário
usuario = input('Digite seu Nome: ').strip()
senha = input('Digite sua Senha: ').strip()

query = "SELECT id_usuario, nm_usuario, altura, peso, idade, sexo FROM usuario WHERE nm_usuario = %s AND senha = %s"
cursor.execute(query, (usuario, senha))
usuario_encontrado = cursor.fetchone()

if usuario_encontrado:
    print("Seja bem-vindo", usuario)
    id_usuario, nome, altura, peso, idade, sexo = usuario_encontrado

else:
    print("Usuário ou senha incorretos")
    login = input("Deseja criar uma nova conta ? (Sim / Nao) ").strip().lower()
    if login == "sim":
        altura = float(input('Digite sua altura em metros (ex: 1.75): '))
        peso = float(input('Digite seu peso em Kg: '))
        idade = int(input('Digite sua idade: '))
        sexo = input('Digite seu sexo (Masculino | Feminino): ').strip().capitalize()
        while sexo not in ['Masculino', 'Feminino']:
            print("Sexo inválido. Digite 'Masculino' ou 'Feminino'.")
            sexo = input('Digite seu sexo (Masculino | Feminino): ').strip().capitalize()

        cmd = "INSERT INTO usuario (nm_usuario, senha, altura, peso, idade, sexo) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(cmd, (usuario, senha, altura, peso, idade, sexo))
        cnn.commit()
        id_usuario = cursor.lastrowid
        print("Conta criada com sucesso!")
    else:
        print("Programa finalizado. 👋")
        exit()

# Função para registrar histórico
def registrar_historico(tipo, last_id):
    if tipo == 'cardio':
        cmd_hist = "INSERT INTO historico (dia, cardio_id, id_usuario) VALUES (NOW(), %s, %s)"
    elif tipo == 'musculacao':
        cmd_hist = "INSERT INTO historico (dia, id_treino, id_usuario) VALUES (NOW(), %s, %s)"
    cursor.execute(cmd_hist, (last_id, id_usuario))
    cnn.commit()

# Menu principal
while True:
    print("\n=== MENU PRINCIPAL ===")
    print("1 - Registrar Exercício")
    print("2 - Calcular IMC/TMB/Gasto calórico diário")
    print("3 - Meus últimos exercícios")
    print("4 - Sair")

    opcao = input("Escolha uma opção: ").strip()

    # OPÇÃO 1: Registrar Exercício
    if opcao == "1":
        exercicios = {
            "1": "Corrida (5:35 min/km)",
            "2": "Caminhada",
            "3": "Natação",
            "4": "Ciclismo",
            "5": "Musculação"
        }
        met_dict = {
            '1': 10.5,  # Corrida
            '2': 4.0,   # Caminhada
            '3': 8.0,   # Natação
            '4': 7.0,   # Ciclismo
            '5': 6.0    # Musculação
        }

        print("1 - Corrida (5:35 min/km)\n2 - Caminhada\n3 - Natação\n4 - Ciclismo\n5 - Musculação")
        exerc = input('Digite o número do exercício: ').strip()

        # Exercícios aeróbicos (cardio)
        if exerc in exercicios and exerc != "5":
            nome_exercicio = exercicios[exerc]
            duracao = float(input('Digite a duração do exercício em minutos: '))
            ritimo = input('Digite o ritmo médio (min/km) no formato mm:ss: ').strip()
            intensidade = input('Digite a intensidade (leve, moderada, intensa): ').strip().lower()

            gasto_calorico = (met_dict[exerc] * peso * duracao) / 60

            cmd = """
            INSERT INTO atv_cardio (nm_exercicio, tempo_atv, ritimo_medio, gasto_calorico, id_usuario)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(cmd, (nome_exercicio, f"00:{int(duracao):02}:00", f"00:{ritimo}", gasto_calorico, id_usuario))
            cnn.commit()

            cardio_id = cursor.lastrowid
            registrar_historico('cardio', cardio_id)
            print(f"{nome_exercicio} registrado com sucesso!")

        # Musculação
        elif exerc == '5':
            exercicio_nome = input('Digite o nome do exercício: ').strip()
            peso_exerc = float(input('Digite o peso levantado em Kg: '))
            repeticoes = int(input('Digite o número de repetições: '))
            series = int(input('Digite o número de séries: '))
            tempo_treino = float(input('Digite o tempo total de treino em minutos: '))

            gasto_calorico = met_dict['5'] * peso * (tempo_treino / 60)

            cmd = """
            INSERT INTO treino (exercicio, atv_peso, repeticoes, series, tempo, gasto_calorico, id_usuario)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(cmd, (exercicio_nome, peso_exerc, repeticoes, series, f"00:{int(tempo_treino):02}:00", gasto_calorico, id_usuario))
            cnn.commit()

            treino_id = cursor.lastrowid
            registrar_historico('musculacao', treino_id)
            print(f"{exercicio_nome} registrado com sucesso!")

        else:
            print("Opção de exercício inválida.")

    # OPÇÃO 2: Calcular IMC/TMB/Gasto calórico diário
    elif opcao == "2":
        menu = input("Selecione uma das opções (IMC ou TMB): ").strip().upper()
        if menu == "IMC":
            imc = peso / (altura ** 2)
            print(f"Seu IMC é de: {imc:.2f}")
            if imc < 18.5:
                print('Você está abaixo do peso ideal.')
            elif imc < 24.9:
                print('Você está com o peso ideal.')
            elif imc < 29.9:
                print('Você está com sobrepeso.')
            elif imc < 34.9:
                print('Você está com Obesidade Grau I.')
            elif imc < 39.9:
                print('Você está com Obesidade Grau II.')
            else:
                print('Você está com Obesidade Grau III.')

        elif menu == "TMB":
            exerc_p_semana = int(input('Quantas vezes por semana você pratica exercícios físicos? '))
            if sexo == 'Masculino':
                tmb = 66 + (13.7 * peso) + (5 * altura * 100) - (6.8 * idade)
            else:
                tmb = 655 + (9.6 * peso) + (1.8 * altura * 100) - (4.7 * idade)

            if exerc_p_semana <= 2:
                f_ativ = 1.2
            elif exerc_p_semana <= 4:
                f_ativ = 1.35
            elif exerc_p_semana <= 6:
                f_ativ = 1.55
            else:
                f_ativ = 1.7

            gasto_diario = tmb * f_ativ
            print(f'Seu gasto calórico diário estimado é de: {round(gasto_diario)} kcal')

        else:
            print("Opção inválida.")

    # OPÇÃO 3: Mostrar últimos 5 exercícios
    elif opcao == "3":
        print("\n=== SEUS ÚLTIMOS EXERCÍCIOS ===")
        cmd = """
        SELECT 
            h.dia,
            t.exercicio,
            t.atv_peso,
            t.repeticoes,
            t.series,
            t.gasto_calorico,
            c.nm_exercicio,
            c.tempo_atv,
            c.ritimo_medio,
            c.gasto_calorico
        FROM historico h
        LEFT JOIN treino t ON t.id_treino = h.id_treino
        LEFT JOIN atv_cardio c ON c.cardio_id = h.cardio_id
        WHERE h.id_usuario = %s
        ORDER BY h.dia DESC
        LIMIT 5;
        """
        cursor.execute(cmd, (id_usuario,))
        registros = cursor.fetchall()

        if not registros:
            print("Nenhum exercício registrado ainda.")
        else:
            for row in registros:
                dia = row[0]
                # Musculação
                if row[1] is not None:
                    print(f"""
📌 {dia}
💪 Musculação: {row[1]}
• Peso: {row[2]} kg
• Repetições: {row[3]}
• Séries: {row[4]}
🔥 Gasto calórico: {row[5]:.2f} kcal
---------------------------------------------""")
                # Cardio
                else:
                    print(f"""
📌 {dia}
🏃 Cardio: {row[6]}
• Tempo: {row[7]}
• Ritmo médio: {row[8]}
🔥 Gasto calórico: {row[9]:.2f} kcal
---------------------------------------------""")

    # OPÇÃO 4: Sair
    elif opcao == "4":
        print("Finalizando Programa... 👋")
        break

    else:
        print("Opção inválida! Tente novamente.")
# Fechando a conexão com o banco de dados
cursor.close()
cnn.close()