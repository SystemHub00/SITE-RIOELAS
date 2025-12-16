/*
Arquivo: static/assistant.js
Descrição: Script para exibir um assistente virtual com instruções passo a passo no site.
*/


// Define mensagens diferentes para cada página
let steps = [];
const path = window.location.pathname;
if (path === '/' || path === '/index' || path === '/index.html') {
  steps = [
    'Bem-vinda ao Rio+Elas! Para começar, clique no botão <b>Quero me inscrever agora!</b> logo abaixo.',
    'Esse botão vai te levar para o formulário de inscrição. Clique nele para continuar.'
  ];
} else if (path.startsWith('/inscricao')) {
  steps = [
    'Preencha seu <b>Nome Completo</b> igual está no seu documento.',
    'Selecione seu <b>Gênero</b> na lista.',
    'Digite seu <b>CPF</b> (apenas números, o sistema coloca os pontos automaticamente).',
    'Digite sua <b>Data de Nascimento</b> (só os números). O sistema coloca as barras automaticamente!',
    'Coloque seu <b>WhatsApp</b> para contato. Lembre-se de colocar o <b>DDD do seu estado</b> antes do número!',
    'Digite seu <b>Email</b> para receber informações importantes.',
    'Quando terminar, clique em <b>PRÓXIMO →</b> para avançar.'
  ];
} else if (path.startsWith('/endereco')) {
  steps = [
    'Agora preencha seu <b>endereço completo</b> para continuarmos.',
    'Digite o <b>CEP</b> corretamente. Se não souber, consulte no site dos Correios.',
    'Preencha o <b>nome da rua</b> e o <b>número</b> da sua residência.',
    'Informe o <b>bairro</b> e a <b>cidade</b> onde você mora.',
    'Selecione o <b>estado</b> na lista.',
    'Se houver complemento (apto, bloco, etc.), preencha também.',
    'Quando terminar, clique em <b>PRÓXIMO →</b> para avançar.'
  ];
} else if (path.startsWith('/curso')) {
  steps = [
    'Agora escolha o <b>local</b> onde você quer fazer o curso.',
    'Depois, selecione o <b>curso</b> de sua preferência. Os cursos disponíveis mudam conforme o local escolhido.',
    'Por fim, escolha a <b>turma</b> (data e horário) que melhor se encaixa para você.',
    'Quando terminar, clique em <b>PRÓXIMO →</b> para avançar.'
  ];
} else if (path.startsWith('/revisao')) {
  steps = [
    'Revise todos os seus dados com atenção. Não esqueça de preencher o campo <b>Como conheceu o projeto</b>.',
    'Antes de finalizar, marque a caixinha de <b>confirmação dos dados</b> para garantir que está tudo correto.',
    'Se estiver tudo certo, clique em <b>CONFIRMAR INSCRIÇÃO</b> para finalizar.'
  ];
} else if (path.startsWith('/confirmacao')) {
  steps = [
    'Inscrição realizada com sucesso! Guarde o <b>número de protocolo</b> e aguarde a equipe Rio+Elas entrar em contato.'
  ];
} else {
  steps = [
    'Bem-vindo! Use o assistente para receber orientações passo a passo.'
  ];
}

let currentStep = 0;

function showAssistant() {
  let assistant = document.getElementById('assistant-box');
  if (!assistant) {
    assistant = document.createElement('div');
    assistant.id = 'assistant-box';
    assistant.innerHTML = `
      <div id="assistant-avatar">🤖</div>
      <div id="assistant-text"></div>
      <button id="assistant-prev">Anterior</button>
      <button id="assistant-next">Próximo</button>
      <button id="assistant-close">Fechar</button>
    `;
    document.body.appendChild(assistant);
    document.getElementById('assistant-prev').onclick = prevStep;
    document.getElementById('assistant-next').onclick = nextStep;
    document.getElementById('assistant-close').onclick = closeAssistant;
  }
  updateAssistant();
}


function updateAssistant() {
  // Permite HTML nas mensagens (ex: <b>texto</b>)
  document.getElementById('assistant-text').innerHTML = steps[currentStep];
  document.getElementById('assistant-prev').disabled = currentStep === 0;
  document.getElementById('assistant-next').disabled = currentStep === steps.length - 1;
}

function nextStep() {
  if (currentStep < steps.length - 1) {
    currentStep++;
    updateAssistant();
  }
}

function prevStep() {
  if (currentStep > 0) {
    currentStep--;
    updateAssistant();
  }
}

function closeAssistant() {
  document.getElementById('assistant-box').remove();
}

// Ícone flutuante para abrir o assistente
window.onload = function() {
  // Mostra o assistente automaticamente ao carregar a página
  showAssistant();
  // Cria o ícone para reabrir caso o usuário feche
  let icon = document.createElement('div');
  icon.id = 'assistant-icon';
  icon.innerText = '🤖';
  icon.title = 'Precisa de ajuda? Clique aqui!';
  icon.onclick = showAssistant;
  document.body.appendChild(icon);
};
