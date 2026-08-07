<a id="readme-top"></a>



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Email Summariser</h3>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

A small desktop app that fetches your recent emails, sends them to Claude for summarisation, and shows the results in a native window with the summary streaming in as it's generated.

Built as a personal learning project

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites
* Python 3
* An Anthropic API key
* A Google Cloud project with the Gmail API enabled and OAuth credentials

### Installation

1. Get an API Key at Anthropic's website and make sure credits are tied to it. The Anthropic API key is kept in the system keyring rather than in code;
2. Clone the repo
   ```sh
   git clone https://github.com/github_username/email-summariser.git
   cd email-summariser
   pip install -r requirements.txt
   ```
4. Set up Google OAuth. In the Google Cloud Console, enable the Gmail API and create OAuth client credentials. Add yourself as a test user on the consent screen, then download the credentials file into the project.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/DV155/email-summariser/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=DV155/email-summariser" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the MIT license. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
