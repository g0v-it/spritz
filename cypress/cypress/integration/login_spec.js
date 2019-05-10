describe('Login Test', function() {
    it('login as aldo', function() {
        // login
        cy.visit('/lang/uk')  
        cy.visit('/login')  
        cy.get('#user_name').type('aldo')
        cy.get('#pass_word').type('aldo')
        cy.get('button').click()
        cy.get('.alert-success')
        // logout
        cy.get('[data-cy=logoff]').click()
        cy.get('h1').contains('Logout')
    })
    it('login by request', function() {
        // login
        cy.request({
            method: 'POST',
            url: '/login', // baseUrl is prepended to url
            form: true, // indicates the body should be form urlencoded and sets Content-Type: application/x-www-form-urlencoded headers
            body: {
              user_name: 'aldo',
              pass_word: 'aldo'
            }
        })
        cy.visit('/votation_list')
        cy.get('h1').contains('Votations list')
    })

    it('Wrong login', function() {
        // login
        cy.visit('/lang/uk')  
        cy.visit('/login')  
        cy.get('#user_name').type('aldo')
        cy.get('#pass_word').type('wrong password')
        cy.get('button').click()
        cy.get('.alert-danger')
    })

})

