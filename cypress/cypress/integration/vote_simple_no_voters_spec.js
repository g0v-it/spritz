describe('voting simple majority  (no voters) Test', function() {
    beforeEach(function () {
        cy.login('aldo', 'aldo')
        cy.visit('/lang/uk')
        cy.createvotation('during','simple')
    })
    afterEach(function () {
        cy.deletefirstvotation()
        cy.visit('/logout')
    })

    it('vote a simple majority  (no voters)', function() {
        
        // go in the votation and get the first ID
        cy.visit("/votation_list")
        cy.get('[data-cy=votation_id]').first().then(($span) => {
            const votation_id = $span.text()
            // set a vote
            cy.visit("/vote/" + votation_id)
            cy.get("[data-cy=radio]").first().check()
            cy.get("[data-cy=password]").type("aa")
            cy.get("[data-cy=submit]").click()
            cy.get('.alert-success').should('contain', 'Your vote has been registered')

            // set the end_date and time so you can close
            const new_end_date = Cypress.moment().utc().format("YYYY-MM-DD")
            const new_end_time = Cypress.moment().utc().subtract(2,'m').format("HH:mm")
            //cy.wait(1000 * 120)

            cy.updateenddate(votation_id, new_end_date,new_end_time)
    
            // check for counters
            cy.visit("/votation_list")
            cy.get('[data-cy=detail]').first().click()
            cy.get('[data-cy=count_voters]').should('contain', '1')        
            cy.get('[data-cy=count_votes]').should('contain', '1')        

            // close the votation
            cy.get('[data-cy=close]').click()        
            cy.get('.alert-success').should('contain', 'Election closed')

        })
    })

    it('wrong vote password  (no voters)', function() {
        
        // go in the votation and get the first ID
        cy.visit("/votation_list")
        cy.get('[data-cy=votation_id]').first().then(($span) => {
            const votation_id = $span.text()
            // set a vote
            cy.visit("/vote/" + votation_id)
            cy.get("[data-cy=radio]").first().check()
            cy.get("[data-cy=password]").type("aa")
            cy.get("[data-cy=submit]").click()
            cy.get('.alert-success').should('contain', 'Your vote has been registered')
            // set a vote but with wrong password
            cy.visit("/vote/" + votation_id)
            cy.get("[data-cy=radio]").first().check()
            cy.get("[data-cy=password]").type("bb")
            cy.get("[data-cy=submit]").click()
            cy.get('.alert-danger').should('contain', 'Error')
            
    
        })
    })

    it('vote two different users  (no voters)', function() {
        
        // aldo voting
        cy.visit("/votation_list")
        cy.get('[data-cy=votation_id]').first().then(($span) => {
            const votation_id = $span.text()
            // aldo set a vote
            cy.visit("/vote/" + votation_id)
            cy.get("[data-cy=radio]").first().check()
            cy.get("[data-cy=password]").type("aa")
            cy.get("[data-cy=submit]").click()
            cy.get('.alert-success').should('contain', 'Your vote has been registered')

            // change user
            cy.login('beppe', 'beppe')
            cy.visit('/lang/uk')
            // beppe set a vote 
            cy.visit("/vote/" + votation_id)
            cy.get("[data-cy=radio]").first().check()
            cy.get("[data-cy=password]").type("bb")
            cy.get("[data-cy=submit]").click()
            cy.get('.alert-success').should('contain', 'Your vote has been registered')

            // aldo, again
            cy.login('aldo', 'aldo')
            cy.visit('/lang/uk')
            
            // set the end_date and time so you can close
            const new_end_date = Cypress.moment().utc().format("YYYY-MM-DD")
            const new_end_time = Cypress.moment().utc().subtract(2,'m').format("HH:mm")
            //cy.wait(1000 * 120)

            cy.updateenddate(votation_id, new_end_date,new_end_time)
    
            // check for counters
            cy.visit("/votation_list")
            cy.get('[data-cy=detail]').first().click()
            cy.get('[data-cy=count_voters]').should('contain', '2')        
            cy.get('[data-cy=count_votes]').should('contain', '2')        

            // close the votation
            cy.get('[data-cy=close]').click()        
            cy.get('.alert-success').should('contain', 'Election closed')

        })
    })


})

