# Aura & Bloom - Testing

## Contents

- [Automated Testing](#automated-testing)
    - [W3C Validator](#w3c-validation)
    - [Lighthouse](#lighthouse)
    - [JSLint](#jslint)
    - [Python Pep8 Checker](#pep8checker)
    - [Lighthouse](#lighthouse)
- [Manual Testing](#manual-testing)
    - [Testing User Stories](#testing-user-stories)
    - [Further Tests](#further-tests)


### Automated Testing

I aimed to use python test files within the project, however when writing the tests, I ran into an issue where I couldn't test my booking form due to the ServicesList model having an image field and I was unable to wrap my head around adding a fake image to that test, so I had to stick to manual testing.

#### W3C Validatior

I used W3C validation for both the html and the css.

![HTML Validation - Appointments](/readme/testing/validation/appointments_page_html_val.JPG)

![HTML Validation - Contacts](/readme/testing/validation/contact_page_html_val.JPG)

![HTML Validation - Homepage](/readme/testing/validation/homepage_html_val.JPG)

![CSS Validation](/readme/testing/validation/css_validator.JPG)

#### JSLint

I used [https://www.jslint.com/] to check my javascript, however it threw errors especially with the checkout.js file, with a lot of those being linked to how stripe document the scripting themselves. So I went with what the documentation suggested, especially around what JSLint sees as trailing commas, which may have proved needed from Stripe's perspective.

![JSLint Validation](/readme/testing/validation/jslint_validation.JPG)

#### Python Pep8 Checker

I used Code Institute's Python validator to run my python through, however I also used VS Code's built in 'problems' tab on the terminal to go through and make sure I had sorted out all issues I could. I opted to leave unused Python files within the project, just for ease in future if I decided to use them.

![Python Validation - Appointments Views](/readme/testing/validation/appointments_models_validation.JPG)

![Python Validation - Services Views](/readme/testing/validation/services_models_validation.JPG)

#### Lighthouse

The lighthouse scores were not great, accessibility was good throughout the site which was noticed, but it had issues with loading and highlighted issues specifically surrounding Cloudinary and the Stripe JS inclusion.

![Desktop Lighthouse](/readme/testing/validation/lighthouse_desktop.JPG)

![Mobile Lighthouse](/readme/testing/validation/mobile_lighthouse.JPG)

### Manual Testing

#### Testing User Stories

| Goals | How are they achieved? |
| :--- | :--- |
| As a Site Owner/Admin I can add and edit services so that users can select them. | I needed to create a model which the site owner can then add services to, and then subsequently edit/delete them when needed. When building this it also included having to create a Category model and use them alongside each other, so that if a new category of service was needed then that could be easily created. |
| As the site owner/admin I want to view all bookings so that I can filter through upcoming. | With this story, I needed to create a way for the site owner to be able to view bookings. So far the bookings can be viewed, however cannot currently be filtered to display only upcoming, or even just this month's bookings, that will be planned for later implementation. |
| As a site user I can create an account so that I can view and track my appointments. | For this story, I created an account page that then would display a user's bookings when they've been made. |
| As a site user I want to filter through services so that I can pick specific categories to look at. | For this story, the services page offers two means of filtering, the first is by simply sorting A-Z or by Category A-Z, or the user can select a specific category they want to see more services for and then they will get filterd. |
| As a site user, I want to confirm a booking with the site owner so that I can view it after making it. | This story was then built around the payment system, generating a booking id for the user to then have, as well as making sure they'd be able to view their bookings after they've been made was key. |

#### Further Tests





