def generate_story(prompt):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": f"Buat cerita anak dari ide berikut:\n{prompt}\n\nGunakan bahasa sederhana dan menarik."
            }
        ]
    )
    return response.choices[0].message.content


# ======================
# FUNCTION: Generate Image
# ======================
def generate_image(prompt):
    image_url = f"https://image.pollinations.ai/prompt/{prompt}"
    return image_url