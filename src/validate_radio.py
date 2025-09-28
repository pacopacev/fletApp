
class ValidateRadio:
    def __init__(self):
        pass

    async def validate_stream(self, url):
        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                async with session.get(url, allow_redirects=False) as response:
                    print(f"Status: {response.status}")
                    print(f"Headers: {dict(response.headers)}")
                    
                    # Check for redirect
                    if response.status in [301, 302, 303, 307, 308]:
                        redirect_url = response.headers.get('Location')
                        print(f"Redirecting to: {redirect_url}")
                        # You could choose to follow it manually or return the redirect URL
                        return True, redirect_url  # Modified return to include info
                    
                    if response.status == 200 and 'audio' in response.headers.get('Content-Type', ''):
                        url = response.url
                        return True, response.url
                    else:
                        return False, None
                        
        except Exception as e:
            print(f"Error validating stream: {e}")
            return False, None