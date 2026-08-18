// Array com as perguntas do Quiz sobre Parnamirim
const perguntasQuiz = [
  {
    pergunta: "1) Por que Parnamirim ficou conhecida como 'Trampolim da Vitória'?",
    opcoes: [
      { texto: "Pela produção de café e açúcar", correta: false },
      { texto: "Pela base aérea americana estratégica na Segunda Guerra", correta: true },
      { texto: "Pela criação do primeiro porto do estado", correta: false }
    ]
  },
  {
    pergunta: "2) Em qual ano foi fundado o Centro de Lançamento da Barreira do Inferno (CLBI)?",
    opcoes: [
      { texto: "1965", correta: true },
      { texto: "1980", correta: false },
      { texto: "2000", correta: false }
    ]
  },
  {
    pergunta: "3) O Cajueiro de Pirangi, conhecido como o maior do mundo, fica em qual município?",
    opcoes: [
      { texto: "Natal", correta: false },
      { texto: "Parnamirim", correta: true },
      { texto: "Macaíba", correta: false }
    ]
  }
];

let indicePerguntaAtual = 0;
let pontuacaoFinal = 0;

// Elementos do HTML
const elementoPergunta = document.querySelector('.pergunta');
const containerOpcoes = document.querySelector('.opcoes');
const caixaFeedback = document.getElementById('mensagem-feedback');

// Função para carregar a pergunta na tela
function carregarPergunta() {
  const dadosAtual = perguntasQuiz[indicePerguntaAtual];
  
  // Atualiza o texto da pergunta
  elementoPergunta.innerHTML = `<strong>${dadosAtual.pergunta}</strong>`;
  
  // Limpa as opções anteriores
  containerOpcoes.innerHTML = '';
  caixaFeedback.classList.add('oculto');

  // Cria os botões para cada opção
  dadosAtual.opcoes.forEach(opcao => {
    const botao = document.createElement('button');
    botao.classList.add('btn-resposta');
    botao.textContent = opcao.texto;
    
    botao.addEventListener('click', () => checarResposta(opcao.correta));
    containerOpcoes.appendChild(botao);
  });
}

// Função para checar a resposta e avançar
function checarResposta(ehCorreta) {
  if (ehCorreta) {
    pontuacaoFinal++;
  }

  indicePerguntaAtual++;

  // Se ainda houver perguntas, carrega a próxima. Se não, mostra o resultado final.
  if (indicePerguntaAtual < perguntasQuiz.length) {
    carregarPergunta();
  } else {
    mostrarResultadoFinal();
  }
}

// Função para exibir a pontuação total
function mostrarResultadoFinal() {
  elementoPergunta.innerHTML = `<strong>Quiz Concluído!</strong>`;
  containerOpcoes.innerHTML = '';
  
  caixaFeedback.classList.remove('oculto', 'erro');
  caixaFeedback.classList.add('acerto');
  caixaFeedback.innerHTML = `Você acertou <strong>${pontuacaoFinal}</strong> de <strong>${perguntasQuiz.length}</strong> perguntas! 🎉`;
}

// Inicializa a primeira pergunta ao carregar
carregarPergunta();