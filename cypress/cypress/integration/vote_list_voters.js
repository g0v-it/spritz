describe('List of voters Testing', function() {
    beforeEach(function () {
        cy.login('aldo', 'aldo')
        cy.visit('/lang/uk')
        cy.createvotation('during','simple',"cat\ndog\nbird\nfish",true)
    })
    afterEach(function () {
        cy.login('aldo', 'aldo')
        cy.deletefirstvotation()
        cy.visit('/logout')
    })

    it('you are on the list', function() {        
        // put two voters
        cy.visit("/votation_list")
        cy.get('[data-cy=detail]').first().click()
        cy.get('[data-cy=isnt_voter]')
        cy.get('#list_voters').type("aldo\nbeppe")
        cy.get('[data-cy=add_voter_button]').click()
        cy.get('.alert-success')

        // put a duplicate
        cy.visit("/votation_list")
        cy.get('[data-cy=detail]').first().click()
        cy.get('[data-cy=is_voter]')
        cy.get('#list_voters').type("aldo\nbeppe")
        cy.get('[data-cy=add_voter_button]').click()
        cy.get('.alert-success')

        // put another voter
        cy.visit("/votation_list")
        cy.get('[data-cy=detail]').first().click()
        cy.get('[data-cy=is_voter]')
        cy.get('#list_voters').type("carlo")
        cy.get('[data-cy=add_voter_button]').click()
        cy.get('.alert-success')

        // beppe should be a voter
        cy.login('beppe','beppe')
        cy.visit("/votation_list")
        cy.get('[data-cy=detail]').first().click()
        cy.get('[data-cy=is_voter]')

        // carlo should be a voter
        cy.login('carlo','carlo')
        cy.visit("/votation_list")
        cy.get('[data-cy=detail]').first().click()
        cy.get('[data-cy=is_voter]')

    })

    it('you are not on the list', function() {        
        // put three voters
        cy.visit("/votation_list")
        cy.get('[data-cy=detail]').first().click()
        cy.get('[data-cy=isnt_voter]')
        cy.get('#list_voters').type("aldo\nbeppe\ncarlo")
        cy.get('[data-cy=add_voter_button]').click()
        cy.get('.alert-success')

        // dario shouldn't be a voter
        cy.login('dario','dario')
        cy.visit("/votation_list")
        cy.get('[data-cy=detail]').first().click()
        cy.get('[data-cy=isnt_voter]')
    })

    it('you can vote', function() {        
        // put three voters
        cy.visit("/votation_list")
        cy.get('[data-cy=detail]').first().click()
        cy.get('#list_voters').type("aldo\nbeppe\ncarlo")
        cy.get('[data-cy=add_voter_button]').click()
        cy.get('.alert-success')

        // beppe can vote
        cy.login('beppe','beppe')
        cy.visit("/votation_list")
        cy.get('[data-cy=vote]').first().click()
        cy.get('#vote_key')
    })
    it('you cannot vote', function() {        
        // put three voters
        cy.visit("/votation_list")
        cy.get('[data-cy=detail]').first().click()
        cy.get('#list_voters').type("aldo\nbeppe\ncarlo")
        cy.get('[data-cy=add_voter_button]').click()
        cy.get('.alert-success')

        // beppe can vote
        cy.login('dario','dario')
        cy.visit("/votation_list")
        cy.get('[data-cy=vote]').first().click()
        cy.get('[data-cy=isnt_voter]')
    })

})

