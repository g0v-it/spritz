describe('voting simple majority Test  (voters)', function() {
    beforeEach(function () {
        cy.login('aldo', 'aldo')
        cy.visit('/lang/uk')
        cy.createvotation('during','simple',"cat\ndog\nbird\nfish",true)
        // put two voters
        cy.visit("/votation_list")
        cy.get('[data-cy=detail]').first().click()
        cy.get('[data-cy=isnt_voter]')
        cy.get('#list_voters').type("aldo\nbeppe")
        cy.get('[data-cy=add_voter_button]').click()
        cy.get('.alert-success')
    })
    afterEach(function () {
        cy.deletefirstvotation()
        cy.visit('/logout')
    })

    it('vote a simple majority (voters)', function() {
        
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

    it('wrong vote password (voters)', function() {
        
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

    it('vote two different users (voters)', function() {
        
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
            cy.get("[data-cy=radio]").eq(1).check()
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

            cy.log("Check if the votes are right")
            cy.visit("/votation_list")
            cy.get('[data-cy=detail]').first().click()

            // A: 2 votes
            // B: 0 votes
            // C: 0 votes
            cy.get('[data-cy=option_counting').first().should('contain', 'BIRD: 1 votes')
            cy.get('[data-cy=option_counting').eq(1).should('contain', 'CAT: 1 votes')
            cy.get('[data-cy=option_counting').eq(2).should('contain', 'DOG: 0 votes')
            cy.get('[data-cy=option_counting').eq(3).should('contain', 'FISH: 0 votes')

        })
    })


})

