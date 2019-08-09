describe('voting majority judgment (voters) Test', function() {
    beforeEach(function () {
        cy.login('aldo', 'aldo')
        cy.visit('/lang/uk')
        cy.createvotation('during','maj_jud',"cat\ndog\nbird\nfish",true)
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


    it('Vote a majority judgment (voters)', function() {
        // go in the votation and get the first ID
        cy.visit("/votation_list")
        cy.get('[data-cy=votation_id]').first().then(($span) => {
            const votation_id = $span.text()

            // set a vote
            cy.visit("/vote/" + votation_id)
            cy.get("[data-cy=word4]").first().check()
            cy.get("[data-cy=password]").type("aa")
            cy.get("[data-cy=submit]").click()
            cy.get('.alert-success').should('contain', 'Your vote has been registered')

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
            cy.get('.alert-success').should('contain', 'Election closed')


        })
    })

    it('Two different votes (voters) ', function() {
        // go in the votation and get the first ID
        cy.visit("/votation_list")
        cy.get('[data-cy=votation_id]').first().then(($span) => {
            const votation_id = $span.text()

            // set a vote
            cy.visit("/vote/" + votation_id)
            cy.get("[data-cy=word4]").first().check()
            cy.get("[data-cy=password]").type("aa")
            cy.get("[data-cy=submit]").click()
            cy.get('.alert-success').should('contain', 'Your vote has been registered')

            // set another vote
            cy.visit("/vote/" + votation_id)
            cy.get("[data-cy=word3]").first().check()
            cy.get("[data-cy=password]").type("aa")
            cy.get("[data-cy=submit]").click()
            cy.get('.alert-success').should('contain', 'Your vote has been registered')

            cy.visit("/votation_list")
            cy.get('[data-cy=detail]').first().click()
            cy.get('[data-cy=count_voters]').should('contain', '1')        
            cy.get('[data-cy=count_votes]').should('contain', '1')        

        })
    })

    it('Wrong password (voters) ', function() {
        // go in the votation and get the first ID
        cy.visit("/votation_list")
        cy.get('[data-cy=votation_id]').first().then(($span) => {
            const votation_id = $span.text()

            // set a vote
            cy.visit("/vote/" + votation_id)
            cy.get("[data-cy=word4]").first().check()
            cy.get("[data-cy=password]").type("aa")
            cy.get("[data-cy=submit]").click()
            cy.get('.alert-success').should('contain', 'Your vote has been registered')

            // set another vote
            cy.visit("/vote/" + votation_id)
            cy.get("[data-cy=word3]").first().check()
            cy.get("[data-cy=password]").type("bb") // <<< WRONG PASSWORD
            cy.get("[data-cy=submit]").click()
            cy.get('.alert-danger').should('contain', 'Error')

            cy.visit("/votation_list")
            cy.get('[data-cy=detail]').first().click()
            cy.get('[data-cy=count_voters]').should('contain', '1')        
            cy.get('[data-cy=count_votes]').should('contain', '1')        

        })
    })


})

