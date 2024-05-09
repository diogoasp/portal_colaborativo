let questionCount = 0;
let answerCount = 0;
let questionController = {}
function captureHTML() {
    const dynamicForm = document.getElementById('dynamic-form');
    const clone = dynamicForm.cloneNode(true);

    // Remove os botões de ação do clone
    const buttons = clone.querySelectorAll('button');
    buttons.forEach(button => button.remove());

    const types = clone.querySelectorAll('select.type-select');
    types.forEach(t => t.remove());

    const labels = clone.querySelectorAll('input.question');
    labels.forEach(l => {
      l.setAttribute('placeholder', l.value);
      x = l.cloneNode();
      x.setAttribute('hidden', true);
      x.setAttribute('name', l.id);
      x.setAttribute('value', l.value);
      x.value = l.value;
      x.htmlContent = l.value;
      x.innerHTML = l.value;
      l.parentNode.appendChild(x);
      l.setAttribute('id', '');
      l.setAttribute('name', '');
      l.setAttribute('readonly', 'True');
    });

    const htmlContent = clone.innerHTML;
    document.getElementById('html_content').value = htmlContent;
}

function submitForm() {
    captureHTML();
    document.forms[0].submit();
}


  function addQuestion() {
      questionCount++;
      const form = document.getElementById('dynamic-form');

      const questionContainer = document.createElement('div');
      questionContainer.classList.add('question-container');

      const question_inputContainer = document.createElement('div');
      question_inputContainer.classList.add('add-container', 'd-flex', 'mb-2');
      const questionInput = document.createElement('input');
      questionInput.placeholder = 'Enter question ' + questionCount;
      questionInput.id = 'question-' + questionCount;
      questionInput.setAttribute('name', 'answer-input-' + questionCount);
      questionInput.classList.add('form-control','question');
      questionInput.type = 'text';
      question_inputContainer.appendChild(questionInput);
      
      const removeQuestionButton = document.createElement('button');
      removeQuestionButton.textContent = 'Remove Question';
      removeQuestionButton.classList.add('btn', 'btn-danger');
      removeQuestionButton.type = 'button';
      removeQuestionButton.onclick = function() {
        questionContainer.remove();
      };
      question_inputContainer.appendChild(removeQuestionButton);
      questionContainer.appendChild(question_inputContainer);

      const addAnswerContainer = document.createElement('div');
      addAnswerContainer.classList.add('add-container', 'd-flex', 'mb-2');

      const typeSelect = document.createElement('select');
      typeSelect.classList.add('form-control', 'type-select');
      typeSelect.innerHTML = `
          <option value="checkbox">Checkbox</option>
          <option value="radio">Radio</option>
          <option value="text">Text</option>
      `;
      addAnswerContainer.appendChild(typeSelect);

      const addAnswerButton = document.createElement('button');
      addAnswerButton.textContent = 'Add Answer';
      addAnswerButton.classList.add('btn', 'btn-primary');
      addAnswerButton.type = 'button'; // Change the type to button
      addAnswerButton.onclick = function() {
          addAnswer(questionContainer, typeSelect.value);
      };
      addAnswerContainer.appendChild(addAnswerButton);

      

      questionContainer.appendChild(addAnswerContainer);

      form.appendChild(questionContainer);
    //   captureHTML();
  }

  function addAnswer(questionContainer, type) {
      answerCount++;
      const answerContainer = document.createElement('div');
      answerContainer.classList.add('answer-container');

      const answerInput = document.createElement('input');
      answerInput.type = type;
      answerInput.placeholder = 'Enter answer';
      answerInput.classList.add('form-control');
      answerInput.id = 'id_answer-input-'+answerCount;
      answerInput.name = 'answer-input-' + questionCount;
      answerContainer.appendChild(answerInput);
      const actionsContainer = document.createElement('div');
      actionsContainer.classList.add('actions');
      
      if (type !== 'text') {
          const label = document.createElement('label');
          label.textContent = 'Label';
          label.id = 'editLabelButton'+answerCount;
          answerContainer.appendChild(label);
          const editLabelButton = document.createElement('button');
          editLabelButton.textContent = 'Edit Label';
          editLabelButton.classList.add('btn', 'btn-secondary');
          editLabelButton.type = 'button';
          editLabelButton.id = 'editLabelButton'+answerCount;
          actionsContainer.appendChild(editLabelButton);
          editLabelButton.onclick = editLabel;
          questionController[editLabelButton.id] = {}
          questionController[editLabelButton.id]['question'] = answerInput
          questionController[editLabelButton.id]['label'] = label
        }
        
      const removeAnswerButton = document.createElement('button');
      removeAnswerButton.textContent = 'Remove';
      removeAnswerButton.classList.add('btn', 'btn-danger');
      removeAnswerButton.type = 'button';
      removeAnswerButton.onclick = function() {
          answerContainer.remove();
      };
      actionsContainer.appendChild(removeAnswerButton);

      answerContainer.appendChild(actionsContainer);

      questionContainer.appendChild(answerContainer);
  }

  function editLabel() {
      const currentLabel = this.textContent;
      $('#newLabelInput').val(currentLabel);
      $('#uptodateLabelInput').val(this.id);
      $('#editModal').modal('show');

      $('#editModal').on('hidden.bs.modal', function () {
          const newLabel = $('#newLabelInput').val().trim();
          if (newLabel !== '') {
            id = $('#uptodateLabelInput').val();
            questionController[id]['label'].textContent = newLabel;
            questionController[id]['question'].value = newLabel;
          }
      });
  }


  function updateLabel() {
    $('#editModal').modal('hide');
  }