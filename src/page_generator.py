import anyio
from html_page_generator import AsyncPageGenerator


async def generate_page(user_prompt: str):
    generator = AsyncPageGenerator()
    with anyio.CancelScope(shield=True):
        async for chunk in generator(user_prompt):
            print(chunk, end="", flush=True)
            yield chunk

        # with open(generator.html_page.title + '.html', 'w', encoding='utf-8') as f:
            # f.write(generator.html_page.html_code)
        with open('generated/index.html', 'w', encoding='utf-8') as f:
            f.write(generator.html_page.html_code)

    print('Файл успешно сохранён!')
