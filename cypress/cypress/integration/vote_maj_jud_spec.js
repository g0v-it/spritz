describe('voting majority judgment Test', function() {
    it('create a majority judgment', function() {
        cy.request({
            method: 'POST',
            url: '/login', 
            form: true, 
            body: {
              user_name: 'aldo',
              pass_word: 'aldo'
            }
        })

        cy.visit("/votation_propose")
        const random_number = Math.trunc( Math.random() * 10000 ) 
        const begin_date = Cypress.moment().utc().format("YYYY-MM-DD")
        const end_date   = begin_date
        const begin_time = Cypress.moment().utc().format("HH:mm")
        const end_time = Cypress.moment().utc().add(2,'m').format("HH:mm")
        cy.get('#votation_description').type('cypress' + random_number)
        cy.get('#votation_type').select('maj_jud')
        cy.get('#begin_date').type(begin_date)
        cy.get('#begin_time').type(begin_time)
        cy.get('#end_date').type(end_date)
        cy.get('#end_time').type(end_time)
        cy.get('#votation_options').type("mare\nmonti\ncampagna")
        cy.get('button').click()
        cy.get('.alert-success').should('contain', 'Votazione salvata')

        cy.visit("/votation_list")
        cy.get('[data-cy=vote]').first().click()
        cy.get("[data-cy=word4]").first().check()
        cy.get("[data-cy=password]").type("aa")
        cy.get('button').click()
        cy.get('.alert-success').should('contain', 'Voto registrato correttamente')
        
        cy.wait(1000 * 120)

        cy.visit("/votation_list")
        cy.get('[data-cy=detail]').first().click()
        cy.get('[data-cy=count_voters]').should('contain', '1')        
        cy.get('[data-cy=count_votes]').should('contain', '1')        

        cy.get('[data-cy=close]').click()        
        cy.get('.alert-success').should('contain', 'Votazione chiusa')


        cy.get("[data-cy=delete_votation]").click()
        cy.get("[data-cy=confirm_delete]").click()
        cy.get('.alert-success').should('contain', 'Votazione cancellata')



    })


})

