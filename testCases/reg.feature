Feature: User Registration

  Scenario: Successful registration with valid details
    Given I am a new user on the registration page
    When I enter a valid name, email, and password
    And I click the 'Register' button
    Then my account should be created
    And I should be redirected to the welcome page

  Scenario: Registration with invalid email format
    Given I am a new user on the registration page
    When I enter a name and password
    And I enter an invalid email format
    And I click the 'Register' button
    Then I should see an error message indicating the email format is invalid
    And my account should not be created

  Scenario: Registration with weak password
    Given I am a new user on the registration page
    When I enter a name and valid email
    And I enter a password that does not meet the strength requirements
    And I click the 'Register' button
    Then I should see an error message indicating the password is too weak
    And my account should not be created