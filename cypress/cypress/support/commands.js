// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
Cypress.Commands.add("login", (username, password) => {
    cy.request({
        method: 'POST',
        url: '/login', 
        form: true, 
        body: {
          user_name: username,
          pass_word: password
        }
    })
})
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This is will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })
Cypress.Commands.add("createvotation", (when,type,options_list="a\nb\nc",list_voters=false) => {
    // when = 'before', 'during' and 'after' voting
    // type = 'simple' or 'maj_jud'
    cy.visit("/votation_propose")
    const delay_minutes = 15
    const random_number = Math.trunc( Math.random() * 10000 ) 
    var begin_date,begin_time,end_date,end_time
    if (when == 'before') {
        begin_date = Cypress.moment().utc().format("YYYY-MM-DD")
        end_date   = begin_date
        begin_time = Cypress.moment().utc().add(  delay_minutes,'m').format("HH:mm")
        end_time   = Cypress.moment().utc().add(2*delay_minutes,'m').format("HH:mm")
    }
    if (when == 'during') {
        begin_date = Cypress.moment().utc().format("YYYY-MM-DD")
        end_date   = begin_date
        begin_time = Cypress.moment().utc().subtract(delay_minutes,'m').format("HH:mm")
        end_time = Cypress.moment().utc().add(delay_minutes,'m').format("HH:mm")
    }
    if (when == 'after') {
        begin_date = Cypress.moment().utc().format("YYYY-MM-DD")
        end_date   = begin_date
        begin_time = Cypress.moment().utc().subtract(2*delay_minutes,'m').format("HH:mm")
        end_time = Cypress.moment().utc().subtract(delay_minutes,'m').format("HH:mm")
    }
    cy.get('#votation_description').type('cypress' + random_number)
    if (type == 'simple') {
        cy.get('#votation_type').select('simple_maj')
    }
    if (type == 'maj_jud') {
        cy.get('#votation_type').select('maj_jud')
    }
    cy.get('#begin_date').type(begin_date)
    cy.get('#begin_time').type(begin_time)
    cy.get('#end_date').type(end_date)
    cy.get('#end_time').type(end_time)
    cy.get('#votation_options').type(options_list)
    if (list_voters) {
        cy.get('#list_voters').check()
    }
    cy.get('button').click()
    cy.get('.alert-success').should('contain', 'Votation data saved')
})

Cypress.Commands.add("deletefirstvotation", () => {
            // delete the first votation in the list
            cy.visit("/votation_list")
            cy.get('[data-cy=detail]').first().click()
            cy.get("[data-cy=delete_votation]").click()
            cy.get("[data-cy=confirm_delete]").click()
            cy.get('.alert-success').should('contain', 'Votation deleted')
})

Cypress.Commands.add("updateenddate", (votation_id,new_end_date,new_end_time) => {
    cy.request({
        method: 'GET',
        url: '/update_end_date/' + votation_id, 
        form: false, 
        qs: {
          end_date: new_end_date,
          end_time: new_end_time
        }
    }).its('body').should('include', 'OK')
})
