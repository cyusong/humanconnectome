// Get forms in order of gene-form, name-form, and title-form:
const forms = document.querySelectorAll('form');

const titleInput = document.getElementById("gene_id");


// Change placeholder text based which button is being hovered over.
const alias_button_events = () => {
    let alias_button = document.querySelector('input[value = Alias]');
    alias_button.addEventListener('mouseover', () => {
        titleInput.placeholder = "e.g., CESA1 (hit 'Enter' to search)";
    })
    alias_button.addEventListener('mouseout', () => {
        titleInput.placeholder = "e.g., CESA (hit 'Enter' to search)";
    })
}

// Attaches event listeners to the gene form.
const gene_form_listeners = () => {
    let form_buttons = forms[0].querySelectorAll('.button');
    let form_actions = (function() {
        let temp = [];
        form_buttons.forEach(button => {
            temp.push(button.getAttribute('formaction'));
        })
        return temp;
    })();
    
    for (let i = 0 ; i < form_buttons.length ; i++) {
        form_buttons[i].addEventListener('click', () => {
            submitGeneForm(event, forms[0], form_actions[i]);
        });
    }
}

// Methods for submitting the gene form via buttons:
function submitGeneForm(event, form, path) {
    if (titleInput.value === "") {
        if (path === '/form/gene_id/alias') {
            titleInput.value = 'ESR1';
        } else {
            titleInput.value = 'ESR1';
        }
    }
    form.submit();
}

function submitNameForm(event, form) {
    const titleInput = document.getElementById("author");
    if (titleInput.value === "") {
        titleInput.value = 'Melissa Fullwood';
    }
    form.submit();
}

function submitTitleForm(event, form) {
    const titleInput = document.getElementById("title");
    if (titleInput.value === "") {
        titleInput.value = '19890323';
    }
    form.submit();
}

function submitFormWith(event, value) {
    event.preventDefault();
    // Submit the form with the clicked value
    const link = event.target;
    const form = link.closest('form');
    const input = form.querySelector('input[type="text"]');
    input.value = value;
    form.submit();
}

window.addEventListener('load', () => {
    alias_button_events();
    gene_form_listeners();

    forms[1].setAttribute('onsubmit', `submitNameForm(event, forms[1])`);
    forms[2].setAttribute('onsubmit', `submitTitleForm(event, forms[2])`);
})

/*
This part of the file contains JavaScript for the help part of the landing page.
*/

// Selects the necessary HTML elements to change / attach event listeners to:
const help_information = document.querySelector('#help-text');
const help_buttons = document.querySelectorAll('.button-group')[1].querySelectorAll('.button');

// Change help information depending on which button is clicked:
const change_help_text = (button, text) => {
    /*
    Alters the appearance of the help button and the help text.
    */
    help_buttons.forEach(b => {
        if (b.innerText.toLowerCase() === text) {
            b.classList.remove('hollow');
        } else {
            b.classList.add('hollow');
        }
    })

    switch (text) {
        case 'word':
            help_text = `
            <p>
                Find all entities that contains the searched query.  For instance, if "ESR1" is searched, this search will find the 
                following entities:
                <ul style = 'color: green;'>
                    <li> ESR1 </li>
                    <li> ESR1 and JUN </li>
                    <li> Epigenetic changes at ESR1 changes </li>
                </ul>
                However, it will not find entities such as:
                <br> <br>
                <ul style = 'color: red;'>
                    <li> ESR2 (i.e., another word) </li>
                </ul>
            </p>`;
            break;
        case 'exact':
            help_text = `
            <p>
                Finds the entity that matches the search query <em> exactly</em>.  For instance, if "ESR1" is searched, this search will find the 
                following entity:
                <ul style = 'color: green;'>
                    <li> ESR1 </li>
                </ul>
                However, it will not find entities such as:
                <br> <br>
                <ul style = 'color: red;'>
                    <li> ESR1 and JUN </li>
                </ul>
            </p>`;
            break;
        case 'alias':
            help_text = `
            <p>
                Finds all gene aliases that are associated with the search query.  For instance, if "ESR1" is searched, this search will find the 
                following entities:
                <ul style = 'color: green;'>
                    <li> ESR1 </li>
                </ul>
            </p>`;
            break;
        case 'substring':
            help_text = `
            <p>
                Finds all entities that contain the search query as a substring.  For instance, if "TAD"(topologically associating domain) is searched, this search will find the 
                following entities:
                <ul style = 'color: green;'>
                    <li> ATAD2 (gene) </li>
                    <li> GATAD1 (gene) </li>
                </ul>
            </p>`;
            break;
        case 'non-alphanumeric':
            help_text = `
            <p>
                Finds all entities that contain the search query followed by a non-alphanumeric character.  For instance, if "ESR1" 
                is searched, this search will find the following entities:
                <ul style = 'color: green;'>
                    <li> MAST4-KD/ESR1-KD </li>
                    <li> ESR1-MUTANT CELLS </li>
                </ul>
                However, it will not find entities such as:
                <br> <br>
                <ul style = 'color: red;'>
                    <li>  </li>
                </ul>
            </p>`;            
            break;
        default:
            help_text = `
            <p>
                Click one of the above buttons to find out more about each search function!
            </p>`;
            break;
    };
    help_information.innerHTML = help_text;
}

// Attach event listeners to each button:
help_buttons.forEach(button => {
    let button_text = button.innerText.toLowerCase();
    button.setAttribute('onclick', `change_help_text('${button}', '${button_text}')`);
    help_buttons[0].click();
})
