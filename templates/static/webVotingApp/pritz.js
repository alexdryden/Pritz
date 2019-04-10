document.getElementById('submit').disabled = true;
document.getElementById('submit').style.backgroundColor = "grey";


$(function() {
    $('#general h2 .counter').text('5');
    var generallen = $("#general-content input[name='votebox']:checked").length;
    if(generallen>0){$("#general h2 .counter").text('('+5-generallen+')');}else{$("#general h2 .counter").text('5');}
});

function updateCounter() {
    var len = $("#general-content input[name='votebox']:checked").length;
	if(len>0){$("#general h2 .counter").text(5-len);}else{$("#general h2 .counter").text('5');}
}

$("#general-content input:checkbox").on("change", function() {
	updateCounter();

});

$(function() {
	$('.select_all').change(function() {
		let checkthis = $(this);
		let checkboxes = $(this).parent().next('ul').find("input[name='votebox']");

		if(checkthis.is(':checked')) {
			checkboxes.attr('checked', true);
		} else {
			checkboxes.attr('checked', false);
		}
        updateCounter();

	});

});


function updateChoice(state, id) {

    let author = document.getElementById(id).previousElementSibling.innerHTML;
    if (document.getElementById(id).checked)
    {
        document.getElementById(id).classList.toggle('checked');
        let choiceItem = document.createElement('li');
        let spacer = document.createElement('br');
        let choiceText = document.createTextNode(author);
        let clearChoiceButton = document.createElement('button');
        clearChoiceButton.setAttribute('id',id + "button");
        clearChoiceButton.innerText = 'x';
        clearChoiceButton.onclick = function(){document.getElementById(id).checked = false; updateCounter();
            enforceMaxChoices(); removeChoice(author, id)};
        choiceItem.appendChild(clearChoiceButton);
        choiceItem.appendChild(choiceText);
        choiceItem.setAttribute('id', author);
        choiceItem.setAttribute('style', 'text-align: left;');
        let choices = document.getElementById('choices');
        choices.insertBefore(choiceItem, choices.lastElementChild);
        choices.insertBefore(spacer, choices.lastElementChild);
    }
    else {
        removeChoice(author, id)

    }
    enforceMaxChoices()


}

function removeChoice(liId, checkboxID) {
    document.getElementById(liId).nextElementSibling.remove();
    document.getElementById(liId).remove();
    document.getElementById(checkboxID).classList.toggle('checked');


}

function enforceMaxChoices() {

    if ($("#general-content input[name='votebox']:checked").length===5)
    {

        document.getElementById('submit').disabled = false;
        document.getElementById('submit').style.backgroundColor = '#4b6f31';

        let remaining = document.getElementById('general-content').getElementsByClassName('form-check-input');
        for (let i=0; i<remaining.length; i++) {

            if (remaining[i].classList.contains('checked')) {;}
            else{remaining[i].setAttribute('disabled', 'disabled');}


        }


    }
    else {
        document.getElementById('submit').disabled = true;
        document.getElementById('submit').style.backgroundColor = 'grey';
        let remaining = document.getElementById('general-content').getElementsByClassName('form-check-input');
        for (let i=0; i<remaining.length; i++) {
            remaining[i].removeAttribute('disabled')
        }

    }
}
