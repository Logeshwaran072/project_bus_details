from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
import time
import pandas as pd

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://www.redbus.in/travels/nbstc")
driver.maximize_window()
time.sleep(3)

actions = ActionChains(driver)
wait = WebDriverWait(driver, 15)


#pagination for last page find and move to nexxt page

try:
    pagination_buttons = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".DC_117_pageTabs"))
    )
    if pagination_buttons:
        last_page_number = int(pagination_buttons[-1].text)  # Get the text of the last pagination button
        print(f"Last page number is: {last_page_number}")
    else:
        print("No last page")
        last_page_number = 1

except Exception as e:
    print("Error finding last page number:", e)
    last_page_number = 1  # Default to 1 if pagination fails


# Function to get text or return empty string if not found
def get_empty_text(element, by, value):
    elements = element.find_elements(by, value)
    return elements[0].text if elements else "0"

# List to store bus data
bus_data = []

for page_number in range(1, last_page_number + 1):
# Get route and route link
    try:
        routes = driver.find_elements(By.CLASS_NAME, "route")  # Finding different routes for the state

        for route in routes:
            route_name = route.text
            route_link = route.get_attribute("href")

            # Open the route in a new tab
            actions.key_down(Keys.CONTROL).click(route).key_up(Keys.CONTROL).perform()
            driver.switch_to.window(driver.window_handles[1])  # Switch to the new window
            time.sleep(10)

            # Check for the "View" button
            try:
                state_find = driver.find_elements(By.XPATH, '//*[@id="result-section"]/div[1]/div/div[2]/div/div[4]/div[2]')
                # Check if elements are found and visible
                if state_find:
                    found_displayed = False
                    for button in state_find:
                        if button.is_displayed():
                            print("Button found and displayed.")
                            view_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[class='button']")))

                            for index, button in enumerate(view_buttons):
                                try:
                                    # Scroll to the button by moving to its location
                                    actions.move_to_element(button).perform()
                                    time.sleep(1)                            
                                    button.click()
                                    print(f"Clicked 'View' button {index + 1}")
                                    time.sleep(3)

                                    # Scroll down the page to load more content
                                    old_page_source = driver.page_source
                                    while True:
                                        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                                        time.sleep(3)
        
                                        new_page_source = driver.page_source
                                        if old_page_source == new_page_source:
                                            break
                                        old_page_source = new_page_source
        
                                except Exception as e:
                                    print(f"Error clicking 'View' button: {e}")
        
                            # Locate the container for each bus detail
                            buses = driver.find_elements(By.CLASS_NAME, "bus-item")
                            print(f"Total buses detected: {len(buses)}")
        
                            # Iterate over each bus container and extract details
                            for bus in buses:
                                try:
                                    bus_name = get_empty_text(bus, By.CLASS_NAME, "travels")
                                    bus_type = get_empty_text(bus, By.CLASS_NAME, "bus-type")
                                    departing_time = get_empty_text(bus, By.CLASS_NAME, "dp-time")
                                    duration = get_empty_text(bus, By.CLASS_NAME, "dur")
                                    reaching_time = get_empty_text(bus, By.CLASS_NAME, "bp-time")
                                    star_rating = get_empty_text(bus, By.CLASS_NAME, "rating")
                                    price = get_empty_text(bus, By.CLASS_NAME, "fare")
                                    seats_available = get_empty_text(bus, By.CLASS_NAME, "seat-left")
        
                                    # Append bus details along with route to the list
                                    bus_data.append([route_name, route_link, bus_name, bus_type, departing_time, duration, reaching_time, star_rating, price, seats_available])
        
                                except Exception as e:
                                    print("Error extracting bus details:", e)
        
                            # Close the current route window and switch back to the main window
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            time.sleep(3)
                            found_displayed = True
                            break                   
                else:
                    print("Button not found")
                    
                    # Scroll down the page to load more content
                    old_page_source = driver.page_source
                    while True:
                        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                        time.sleep(3)
    
                        new_page_source = driver.page_source
                        if old_page_source == new_page_source:
                            break
                        old_page_source = new_page_source
    
                    # Locate the container for each bus detail
                    buses = driver.find_elements(By.CLASS_NAME, "bus-item")
                    print(f"Total buses detected: {len(buses)}")
    
                    # Iterate over each bus container and extract details
                    for bus in buses:
                        try:
                            bus_name = get_empty_text(bus, By.CLASS_NAME, "travels")
                            bus_type = get_empty_text(bus, By.CLASS_NAME, "bus-type")
                            departing_time = get_empty_text(bus, By.CLASS_NAME, "dp-time")
                            duration = get_empty_text(bus, By.CLASS_NAME, "dur")
                            reaching_time = get_empty_text(bus, By.CLASS_NAME, "bp-time")
                            star_rating = get_empty_text(bus, By.CLASS_NAME, "rating")
                            price = get_empty_text(bus, By.CLASS_NAME, "fare")
                            seats_available = get_empty_text(bus, By.CLASS_NAME, "seat-left")
        
                            # Append bus details along with route to the list
                            bus_data.append([route_name, route_link, bus_name, bus_type, departing_time, duration, reaching_time, star_rating, price, seats_available])
        
                        except Exception as e:
                            print("Error extracting bus details:", e)
        
                    # Close the current route window and switch back to the main window
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(3)

            except Exception as e:     
                print(f"An error occurred: {e}")

        # page change
        if page_number < last_page_number :
            try:
                next_page = wait.until(EC.element_to_be_clickable(
                    (By.XPATH,f'//div[contains(@class, "DC_117_pageTabs") and text() = "{page_number + 1}"]')))

                actions.move_to_element(next_page).click().perform()
                time.sleep(3)

            except Exception as e:
                print("no more pages or error:",e)
                break

    except Exception as e:
        print("No more pages or encountered an error:", e)
        break


# Convert collected data to a DataFrame
bus_df = pd.DataFrame(bus_data, columns=["Route Name", "Route Link", "Bus Name", "Bus Type", "Departing Time", "Duration", 
    "Reaching Time", "Star Rating", "Price", "Seats Available"])


# insert state column
bus_df.insert(0,"State Name","NBSTC")



# Save the DataFrame to a CSV file
bus_df.to_csv('NBSTC.csv', index=False)



print(f"Data saved to bus_details_with_route.csv with {len(bus_data)} bus details.")
