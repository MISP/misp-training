# MISP Training Materials

This repository includes all the training materials in use such as

- Core MISP (software and standard) trainings
- Threat intelligence and OSINT training
- Building information sharing communities workshop

All the materials are available with the complete LaTeX source code meant to assist in contributing or extending the training materials. A special attention is given to the open source licensing
given to the materials. We welcome contributions in order to improve the training set for threat intelligence, intelligence gathering and analysis along with specific aspects of information sharing/exchange in information and national security.

## Materials

| Slides (PDF) | Source Code |
| ------------ | ----------- |
| [0-misp-introduction-to-information-sharing](https://www.misp-project.org/misp-training/0-misp-introduction-to-information-sharing.pdf) | [source](https://github.com/MISP/misp-training/tree/master/0-misp-introduction-to-information-sharing) |
| [1-misp-usage](https://www.misp-project.org/misp-training/1-misp-usage.pdf) | [source](https://github.com/MISP/misp-training/tree/master/1-misp-usage) |
| [1.2-misp-integration](https://www.misp-project.org/misp-training/1.2-misp-integration.pdf) | [source](https://github.com/MISP/misp-training/tree/master/1.2-misp-integration) |
| [1.1-misp-viper-integration](https://www.misp-project.org/misp-training/1.1-misp-viper-integration.pdf) | [source](https://github.com/MISP/misp-training/tree/master/1.1-misp-viper-integration) |
| [1.2.1-misp-integration-mail2misp](https://www.misp-project.org/misp-training/1.2.1-misp-integration-mail2misp.pdf) | [source](https://github.com/MISP/misp-training/tree/master/1.2.1-misp-integration-mail2misp) |
| [2-misp-administration](https://www.misp-project.org/misp-training/2-misp-administration.pdf) | [source](https://github.com/MISP/misp-training/tree/master/2-misp-administration) |
| [3-misp-taxonomy-tagging](https://www.misp-project.org/misp-training/3-misp-taxonomy-tagging.pdf) | [source](https://github.com/MISP/misp-training/tree/master/3-misp-taxonomy-tagging) |
| [3.1-misp-modules](https://www.misp-project.org/misp-training/3.1-misp-modules.pdf) | [source](https://github.com/MISP/misp-training/tree/master/3.1-misp-modules) |
| [3.2-misp-galaxy](https://www.misp-project.org/misp-training/3.2-misp-galaxy.pdf) | [source](https://github.com/MISP/misp-training/tree/master/3.2-misp-galaxy) |
| [3.3-misp-object-template](https://www.misp-project.org/misp-training/3.3-misp-object-template.pdf) | [source](https://github.com/MISP/misp-training/tree/master/3.3-misp-object-template) |
| [6.0-misp-dashboard](https://www.misp-project.org/misp-training/6.0-misp-dashboard.pdf) | [source](https://github.com/MISP/misp-training/tree/master/6.0-misp-dashboard) |
| [a.0-contributing](https://www.misp-project.org/misp-training/a.0-contributing.pdf) | [source](https://github.com/MISP/misp-training/tree/master/a.0-contributing) |
| [a.1-devintro](https://www.misp-project.org/misp-training/a.1-devintro.pdf) | [source](https://github.com/MISP/misp-training/tree/master/a.1-devintro) |
| [a.2-pymisp](https://www.misp-project.org/misp-training/a.2-pymisp.pdf) | [source](https://github.com/MISP/misp-training/tree/master/a.2-pymisp) |
| [a.3-misp-feed](https://www.misp-project.org/misp-training/a.3-misp-feed.pdf) | [source](https://github.com/MISP/misp-training/tree/master/a.3-misp-feed) |
| [a.4-best-practices](https://www.misp-project.org/misp-training/a.4-best-practices.pdf) | [source](https://github.com/MISP/misp-training/tree/master/a.4-best-practices) |
| [a.5-decaying-indicators](https://www.misp-project.org/misp-training/a.5-decaying-indicators.pdf) | [source](https://github.com/MISP/misp-training/tree/master/a.5-decaying-indicators) |
| [a.6-forensic](https://www.misp-project.org/misp-training/a.6-forensic.pdf) | [source](https://github.com/MISP/misp-training/tree/master/a.6-forensic) |
| [a.7-rest-API](https://www.misp-project.org/misp-training/a.7-rest-API.pdf) | [source](https://github.com/MISP/misp-training/tree/master/a.7-rest-API) |

### Complementary materials

| Slides (PDF) | Source Code |
| ------------ | ----------- |
| [complete slide desk in one PDF](https://www.misp-project.org/misp-training/misp-training.pdf) | [source](https://github.com/MISP/misp-training/) |
| [MISP training cheat-sheet](https://www.misp-project.org/misp-training/cheatsheet.pdf) | [source](https://github.com/MISP/misp-training/tree/master/training-support/compact-cheatsheet) |
| [MISP feature list (for the trainers)](https://www.misp-project.org/misp-training/usage.pdf) | [source](https://github.com/MISP/misp-training/tree/master/training-support/checklist) |

## Source Code

The full source code of the training slide decks are available. You'll need to have an operating system with a recent installation of LaTeX including latex-beamer to work with them.

To build the complete set of training materials:

~~~~bash
bash build.sh
~~~~

The output directory will contain all the generated PDF files and the PDF file called `misp-training.pdf` which is the complete handout of all the slides.

## License, Attribution and Funding

All the materials are dual-licensed under GNU Affero General Public License version 3 or later and
the Creative Commons Attribution-ShareAlike 4.0 International. You can use either one of the licenses depending
of your use case of the training materials.

The MISP project training materials are co-financed and supported by CIRCL Computer Incident Response Center Luxembourg[](https://www.circl.lu/) and co-financed by a CEF (Connecting Europe Facility) funding under CEF-TC-2016-3 - Cyber Security as *Improving MISP as building blocks for next-generation information sharing*.

![](https://www.misp-project.org/assets/images/en_cef.png)
![](https://www.circl.lu/assets/images/logo.png)

All the source code is available at [https://www.github.com/MISP/misp-training](https://www.github.com/MISP/misp-training).

If you reuse the training materials, don't forget to include the above for attribution.
 
## Contributors in alphabetical order

- Steve Clement [:house:](https://github.com/SteveClement)
- Alexandre Dulaunoy [:house:](https://github.com/adulau)
- Andras Iklody [:house:](https://github.com/iglocska)
- Sami Mokaddem [:house:](https://github.com/mokaddem)
- Sascha Rommelfangen [:house:](https://github.com/rommelfs)
- Christian Studer [:house:](https://github.com/chrisr3d)
- Raphaël Vinot [:house:](https://github.com/rafiot)
- Gerard Wagener [:house:](https://github.com/haegardev)

