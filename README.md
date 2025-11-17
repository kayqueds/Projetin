CREATE DATABASE AppFit;
USE AppFit;

CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nm_usuario VARCHAR(100) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    altura FLOAT NOT NULL,
    peso float NOT NULL,
    idade INT NOT NULL,
    sexo varchar(20)
);
alter table usuario
modify peso float;

UPDATE usuario 
SET sexo = "Masculino"
WHERE id_usuario = 11;

select * from usuario;
INSERT INTO usuario (nm_usuario, senha, altura, peso, idade, sexo) 
VALUES 
('João Silva', 'senha123', 1.75, 75.50, 28, 'Masculino'),
('Maria Oliveira', 'senha456', 1.62, 65.30, 24, 'Feminino'),
('Pedro Costa', 'senha789', 1.80, 82.10, 30, 'Masculino'),
('Ana Souza', 'senha101', 1.68, 58.00, 26, 'Feminino'),
('Carlos Pereira', 'senha202', 1.85, 90.70, 35, 'Masculino'),
('Patricia Almeida', 'senha303', 1.60, 50.40, 22, 'Feminino'),
('Felipe Martins', 'senha404', 1.72, 78.20, 29, 'Masculino'),
('Juliana Lima', 'senha505', 1.70, 68.00, 27, 'Feminino'),
('Lucas Rocha', 'senha606', 1.78, 85.00, 33, 'Masculino'),
('Mariana Santos', 'senha707', 1.65, 54.30, 25, 'Feminino');

CREATE TABLE treino (
    id_treino INT AUTO_INCREMENT PRIMARY KEY,
    exercicio VARCHAR(100) NOT NULL,
    atv_peso float,
    repeticoes INT,
    series int,
    tempo time,
    gasto_calorico FLOAT NOT NULL,
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);
alter table treino
modify tempo time;

select	* from treino;

INSERT INTO treino (exercicio, atv_peso, repeticoes, tempo, gasto_calorico, id_usuario) 
VALUES 
('Supino reto', 50.00, 12, '2023-11-17', 300.50, 1),
('Agachamento', 60.00, 15, '2023-11-17', 350.75, 2),
('Puxada na frente', 40.00, 10, '2023-11-17', 250.00, 3),
('Levantamento terra', 80.00, 8, '2023-11-17', 400.00, 4),
('Rosca direta', 30.00, 12, '2023-11-17', 200.25, 5),
('Flexão de braço', NULL, 20, '2023-11-17', 150.00, 6),
('Barra fixa', NULL, 10, '2023-11-17', 180.00, 7),
('Remada curvada', 50.00, 12, '2023-11-17', 300.10, 8),
('Cadeira extensora', 40.00, 15, '2023-11-17', 220.50, 9),
('Panturrilha no leg press', 40.00, 20, '2023-11-17', 180.00, 10);

create table atv_cardio(

	cardio_id int auto_increment primary key,
    nm_exercicio varchar(100),
    tempo_atv time,
    ritimo_medio time,
    gasto_calorico float,
    id_usuario int,
    foreign key (id_usuario) references usuario (id_usuario)
    
);
select * from atv_cardio;

INSERT INTO atv_cardio (nm_exercicio, tempo_atv, ritimo_medio, gasto_calorico, id_usuario)
VALUES 
('Corrida leve', '00:30:00', '00:05:20', 320, 1),
('Ciclismo', '00:45:00', '00:04:50', 450, 2),
('Caminhada rápida', '00:40:00', '00:06:00', 280, 3),
('Elíptico', '00:35:00', '00:05:10', 390, 4),
('Corrida intensa', '00:25:00', '00:04:00', 500, 5),
('Subir escadas', '00:20:00', '00:03:30', 420, 6),
('Pular corda', '00:15:00', '00:02:50', 480, 7),
('Natação', '00:50:00', '00:05:40', 600, 8),
('Remo ergométrico', '00:30:00', '00:04:40', 350, 9),
('Bike ergométrica', '00:45:00', '00:05:00', 430, 10);



CREATE TABLE historico (
    id_historico INT AUTO_INCREMENT PRIMARY KEY,
    dia DATETIME NOT NULL,
    id_treino INT,
    cardio_id int,
    id_usuario INT,
    foreign key (cardio_id) references atv_cardio (cardio_id),
    FOREIGN KEY (id_treino) REFERENCES treino(id_treino),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

select * from historico;
INSERT INTO historico (dia, id_treino, id_usuario) 
VALUES 
('2023-11-17 08:00:00', 1, 1),
('2023-11-17 09:00:00', 2, 2),
('2023-11-17 10:00:00', 3, 3),
('2023-11-17 11:00:00', 4, 4),
('2023-11-17 12:00:00', 5, 5),
('2023-11-17 13:00:00', 6, 6),
('2023-11-17 14:00:00', 7, 7),
('2023-11-17 15:00:00', 8, 8),
('2023-11-17 16:00:00', 9, 9),
('2023-11-17 17:00:00', 10, 10);
