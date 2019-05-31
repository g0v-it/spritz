describe('Create election Test', function() {
    beforeEach(function () {
        cy.login('aldo', 'aldo')
        cy.visit('/lang/uk')
    })
    afterEach(function () {
        cy.visit('/logout')
    })

    it('create a simple majority', function() {
        cy.visit("/votation_propose")
        const random_number = Math.trunc( Math.random() * 10000 ) 
        cy.get('#votation_description').type('cypress' + random_number)
        cy.get('#description_url').type("https://copernicani.it/Libro_bianco/2-il-metodo-spritz-la-nascita-dei-copernicani/")
        cy.get('#votation_type').select('simple_maj')
        cy.get('#begin_date').type('2019-04-01')
        cy.get('#begin_time').type('13:45')
        cy.get('#end_date').type('2019-04-02')
        cy.get('#end_time').type('14:45')
        cy.get('#votation_options').type("mare\nmonti\ncampagna")
        cy.get('button').click()
        cy.get('.alert-success').should('contain', 'Election data saved')
    })
    it('delete the simple maj', function() {
        cy.visit("/votation_list")
        cy.get('[data-cy=detail]').first().click()
        cy.get("[data-cy=delete_votation]").click()
        cy.get("[data-cy=confirm_delete]").click()
        cy.get('.alert-success').should('contain', 'Election deleted')
    })
    it('duplicate description error', function() {
        cy.visit("/votation_propose")
        cy.get('#votation_description').type('cypress Duplicate description error')
        cy.get('#votation_type').select('simple_maj')
        cy.get('#begin_date').type('2019-04-01')
        cy.get('#begin_time').type('13:45')
        cy.get('#end_date').type('2019-04-02')
        cy.get('#end_time').type('14:45')
        cy.get('#votation_options').type("mare\nmonti\ncampagna")
        cy.get('button').click()
        cy.get('.alert-success').should('contain', 'Election data saved')
        cy.visit("/votation_propose")
        cy.get('#votation_description').type('cypress Duplicate description error')
        cy.get('#votation_type').select('simple_maj')
        cy.get('#begin_date').type('2019-04-01')
        cy.get('#begin_time').type('13:45')
        cy.get('#end_date').type('2019-04-02')
        cy.get('#end_time').type('14:45')
        cy.get('#votation_options').type("cypress\nDuplicate\ndescription\nerror")
        cy.get('button').click()
        cy.get('.alert-danger').should('contain', 'Error, election data NOT saved')
    })
    it('delete the duplicate', function() {
        cy.visit("/votation_list")
        cy.get('[data-cy=detail]').first().click()
        cy.get("[data-cy=delete_votation]").click()
        cy.get("[data-cy=confirm_delete]").click()
        cy.get('.alert-success').should('contain', 'Election deleted')
    })



})

