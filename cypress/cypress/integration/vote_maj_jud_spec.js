describe('voting majority judgment Test', function() {
    it('create a majority judgment', function() {
        cy.login('aldo', 'aldo')

        cy.createvotation('during','maj_jud')
        // go in the votation and get the first ID
        cy.visit("/votation_list")
        cy.get('[data-cy=votation_id]').first().then(($span) => {
            const votation_id = $span.text()

            // set a vote
            cy.visit("/vote/" + votation_id)
            cy.get("[data-cy=word4]").first().check()
            cy.get("[data-cy=password]").type("aa")
            cy.get('button').click()
            cy.get('.alert-success').should('contain', 'Voto registrato correttamente')

            // set the end_date and time so you can close
            const new_end_date = Cypress.moment().utc().format("YYYY-MM-DD")
            const new_end_time = Cypress.moment().utc().subtract(2,'m').format("HH:mm")

            cy.updateenddate(votation_id, new_end_date,new_end_time)
    
            // check for counters
            cy.visit("/votation_list")
            cy.get('[data-cy=detail]').first().click()
            cy.get('[data-cy=count_voters]').should('contain', '1')        
            cy.get('[data-cy=count_votes]').should('contain', '1')        

            // close the votation
            cy.get('[data-cy=close]').click()        
            cy.get('.alert-success').should('contain', 'Votazione chiusa')

            cy.deletefirstvotation()

        })
    })
})

