import os
import base64
import logging

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def setup_credentials():
    """
    Set up credentials for deployment.
    This function handles decoding base64-encoded service account credentials
    which is a common approach for deploying to platforms like Render.
    """
    # Create credentials directory if it doesn't exist
    os.makedirs('credentials', exist_ok=True)
    
    # Check if we have base64-encoded service account credentials
    if 'SERVICE_ACCOUNT_JSON_BASE64' in os.environ:
        try:
            logging.info("Found SERVICE_ACCOUNT_JSON_BASE64 environment variable")
            
            # Decode the base64 string
            json_data = base64.b64decode(os.environ['SERVICE_ACCOUNT_JSON_BASE64']).decode('utf-8')
            
            # Save to file
            service_account_path = 'credentials/service_account.json'
            with open(service_account_path, 'w') as f:
                f.write(json_data)
            
            # Update the environment variable to point to the file
            os.environ['SERVICE_ACCOUNT_PATH'] = service_account_path
            
            logging.info(f"Service account credentials saved to {service_account_path}")
            return True
        except Exception as e:
            logging.error(f"Error setting up service account credentials: {e}")
            return False
    else:
        logging.info("No SERVICE_ACCOUNT_JSON_BASE64 environment variable found, using existing credentials")
        return True

if __name__ == "__main__":
    # This can be run directly to test the credentials setup
    setup_credentials()
