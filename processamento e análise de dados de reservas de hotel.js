const reservas = [
{
cliente: "Ana Souza",
categoria: "comum",
tipoQuarto: "Casal",
valorDiaria: 250,
dias: 2,
cafe: false,
fimDeSemana: false,
promocao: 0
},


{
cliente: "Bruno Lima",
categoria: "gold",
tipoQuarto: "Luxo",
valorDiaria: 400,
dias: 3,
cafe: true,
fimDeSemana: true,
promocao: 0.10
},


{
cliente: "Carla Dias",
categoria: "platinum",
tipoQuarto: "Suíte Premium",
valorDiaria: 600,
dias: 2,
cafe: true,
fimDeSemana: true,
promocao: 0.15
},
{
cliente: "Diego Rocha",
categoria: "comum",
tipoQuarto: "Casal",
valorDiaria: 250,
dias: 4,
cafe: true,
fimDeSemana: false,
promocao: 0.05
}
];

//A função calcularReceitaReserva foi criada para calcular o valor total de cada reserva individualmente. 
// Essa função considera o valor da diária, quantidade de dias, café da manhã, reservas em finais de semana e descontos promocionais.


const calcularReceitaReserva = reserva => {
const valorBase = reserva.valorDiaria * reserva.dias;
const valorCafe = reserva.cafe ? 40 * reserva.dias : 0;
const adicionalFimDeSemana = reserva.fimDeSemana ? valorBase * 0.20 : 0;
const desconto = valorBase * reserva.promocao;
 return valorBase + valorCafe + adicionalFimDeSemana - desconto;
};

//A função totalReservas retorna a quantidade total de reservas cadastradas.
const totalReservas = reservas => reservas.length;

//A função receitaTotal utiliza reduce para somar a receita de todas as reservas.
const receitaTotal = reservas =>
 reservas.reduce((total, reserva) =>
   total + calcularReceitaReserva(reserva), 0);

//A função reservasPorCategoria utiliza filter para selecionar reservas de uma categoria específica de cliente.
const reservasPorCategoria = (reservas, categoria) =>
 reservas.filter(reserva => reserva.categoria === categoria);

//A função reservasComCafe retorna apenas as reservas que incluem café da manhã.
const reservasComCafe = reservas =>
 reservas.filter(reserva => reserva.cafe);

//Também foi criada a função receitaPorTipoQuarto, responsável por agrupar e calcular a receita de cada tipo de quarto.
const receitaPorTipoQuarto = reservas =>
  reservas.reduce((resultado, reserva) => {
    const receita = calcularReceitaReserva(reserva);

    return {
      ...resultado,
      [reserva.tipoQuarto]:
        (resultado[reserva.tipoQuarto] || 0) + receita
    };
  }, {});

 //Além disso, foi implementada uma funcionalidade 
 // responsável por sugerir estratégias para 
 // maximização de lucro do hotel. Essa função 
 // compara receitas obtidas por reservas em finais 
 // de semana e reservas com café da manhã, gerando 
 // sugestões estratégicas para o hotel.
const sugerirEstrategiaLucro = reservas => {
 const receitaCafe =
   receitaTotal(reservasComCafe(reservas));


 const receitaFimDeSemana =
   receitaTotal(
     reservas.filter(reserva => reserva.fimDeSemana)
   );
 if (receitaFimDeSemana > receitaCafe) {
   return "Investir em promoções para finais de semana.";
 }
 return "Incentivar pacotes com café da manhã.";
};


