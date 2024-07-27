import os
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import GithubFileLoader
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from urllib.parse import urlparse

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize the Anthropic Chat model
chat_model = ChatAnthropic(
    model_name="claude-3-haiku-20240307",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def load_github_content(repo_url):
    parsed_url = urlparse(repo_url)
    repo = parsed_url.path.strip('/')
    loader = GithubFileLoader(
        repo=repo, 
        access_token=os.getenv("GITHUB_ACCESS_TOKEN"),
        file_filter=lambda file_path: file_path.endswith(
            (".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".ts", ".jsx", ".tsx", ".json", ".xml", ".yml", ".yaml", ".md", ".txt", ".rst", ".csv", ".sql", ".php", ".rb", ".go", ".sh", ".bat", ".ps1", ".pl", ".scala")
        )
    )
    documents = loader.load()
    return "\n\n".join([doc.page_content for doc in documents])

def load_document(file_path):
    if file_path.lower().endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.lower().endswith('.docx'):
        loader = Docx2txtLoader(file_path)
    elif file_path.lower().endswith('.txt'):
        loader = TextLoader(file_path)
    else:
        raise ValueError("Unsupported file type. Please upload PDF, DOCX, or TXT files.")
    documents = loader.load()
    return "\n\n".join([doc.page_content for doc in documents])

def generate_model_card(content, template):
    prompt = PromptTemplate.from_template(
        f"""You are an AI assistant tasked with creating a model card based on the following content:

{{content}}

Please fill out the following template with the relevant information from the content:

{template}

If you can't find specific information for a section, please write "Information not available" for that section."""
    )

    chain = prompt | chat_model | StrOutputParser()
    return chain.invoke({"content": content})

# Customer template
customer_template = """
# Customer Explainability Card: [Model Name]

## Introduction
- **Purpose**: [Purpose and benefit of the model in layman's terms]

## How It Works
- **Overview**: [How the model works at a high level without technical jargon]
- **Application**: [How the model enhances the product or service]

## Data and Privacy
- **Data Usage**: [Type of data the model uses]
- **Privacy**: [Privacy measures to assure customers]

## High-Level Technical Details
- **AI Technology**: [AI technology powering the model]
- **Integration Framework**: [Framework used for integration]
- **Capabilities**: [Key capabilities of the model]

## Performance
- **User Benefits**: [Direct benefits to the customer]
- **Performance**: [Non-technical summary of the model's performance]

## Deployment and Integration
- **Deployment Environment**: [Where and how the model is deployed]
- **Integration Points**: [How the model integrates with other systems or components]

## Data Processing
- **Local Processing**: [Data processing on the user's device]
- **Third-Party Processing**: [Data sent to cloud servers and for what purposes]
- **Data Security**: [Security measures for data transmission and storage]

## Continuous Improvement
- **Updates**: [Mention that the model is regularly updated for better performance]
- **Feedback**: [Encourage customers to provide feedback to help improve the model]

## Future Enhancements
- **Planned Updates**: [Planned updates or improvements]
- **Long-Term Goals**: [Long-term objectives for the model]

## Contact Information
- **Customer Support**: [Contact Details for Customer Support]
- **Feedback**: [Details on How Customers Can Provide Feedback]
"""

# Internal stakeholder template
internal_template = """
# Internal Stakeholder Explainability Card: [Model Name]

## Model Overview
- **Version**: [Version Number]
- **Owner**: [Team/Individual]
- **Release Date**: [Release Date]

## Objective and Use Case
- **Purpose**: [Primary goal of the model]
- **Application**: [How the model integrates into the product and its benefits]

## Data Information
- **Data Sources**: [List and describe the data sources used]
- **Data Volume**: [Size and scope of the dataset]
- **Data Quality**: [Quality checks and preprocessing steps]

## Model Details
- **Type of Model**: [Type of model]
- **Architecture**: [High-level overview of the model architecture]
- **Training Process**: [Training process and tools used]
- **Evaluation Metrics**: [Metrics used to evaluate model performance]

## Performance
- **Training Performance**: [Metrics from the training phase]
- **Testing Performance**: [Metrics from the testing/validation phase]
- **Benchmarking**: [Performance against baseline or competing models]

## Deployment and Integration
- **Deployment Environment**: [Where and how the model is deployed]
- **Integration Points**: [How the model integrates with other systems or components]
- **Monitoring and Maintenance**: [Monitoring and maintenance plan]

## Data Processing
- **Local Processing**: [Data processing on the user's device]
- **Third-Party Processing**: [Data sent to cloud servers and for what purposes]
- **Data Security**: [Security measures for data transmission and storage]

## Risk and Mitigation
- **Known Risks**: [Potential risks associated with the model]
- **Mitigation Strategies**: [Strategies to mitigate these risks]

## Future Enhancements
- **Planned Updates**: [Planned updates or improvements]
- **Long-Term Goals**: [Long-term objectives for the model]

## Contact Information
- **Primary Contact**: [Name and Contact Details]
- **Support Team**: [Support Team Contact Details]
"""

# Explicitly export the templates
__all__ = ['load_github_content', 'load_document', 'generate_model_card', 'customer_template', 'internal_template']

if __name__ == "__main__":
    # This section is for testing purposes only
    from pprint import pprint

    # Test data
    github_content = load_github_content("openai/openai-cookbook")

    customer_card = generate_model_card(github_content, customer_template)
    internal_card = generate_model_card(github_content, internal_template)

    print("Customer Card:")
    pprint(customer_card)
    print("\nInternal Card:")
    pprint(internal_card)
