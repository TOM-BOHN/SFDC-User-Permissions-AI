import io
from pprint import pprint



config_with_search = types.GenerateContentConfig(
    tools=[types.Tool(google_search=types.GoogleSearch())],
    temperature=0.0,
)


def query_with_grounding():
    chat = client.chats.create(model='gemini-2.0-flash')

    response = chat.send_message(
        message="""strictly search for and use results and citations within the https://help.salesforce.com and https://salesforce.com domains.
        write a complete definitions for the following user permission.
        Ensure that the search identifies the setup of the user permission.
        Ensure that the response identifies the specific **Salesforce Cloud** related to the user permission.
        Ensure that the response identifies the specific **Salesforce Feature** related to the user permission.
        This is a Salesforce user permission and is not related to 3rd part managed packages or connected applications.
        Write the new **Description**  in paragraph format.
        -- **Permission Name:** Allows users to use clauses within documents
        -- **API Name:** ClauseUser
        -- Description:** Allows users to use clauses within documents
        """,
        config=config_with_search,
    )

    return response.candidates[0]

rc = query_with_grounding()

while not rc.grounding_metadata.grounding_supports or not rc.grounding_metadata.grounding_chunks:
    # If incomplete grounding data was returned, retry.
    rc = query_with_grounding()

# Extract the chunks
chunks = rc.grounding_metadata.grounding_chunks
# Print the chunks
for chunk in chunks:
    print(f'{chunk.web.title}: {chunk.web.uri}')
# Extract the support
supports = rc.grounding_metadata.grounding_supports
# Print the Support
for support in supports:
    pprint(support.to_json_dict())

print('################')

# Start the buffer
markdown_buffer = io.StringIO()
# Add a Break
markdown_buffer.write('\n----\n')
# Print the content
markdown_buffer.write(rc.content.parts[0].text)
# Add a Break
markdown_buffer.write('\n----\n')
# Print the text with footnote markers.
markdown_buffer.write("Supported text:\n\n")
for support in supports:
    markdown_buffer.write(" * ")
    markdown_buffer.write(
        rc.content.parts[0].text[support.segment.start_index : support.segment.end_index]
    )

    for i in support.grounding_chunk_indices:
        chunk = chunks[i].web
        markdown_buffer.write(f"<sup>[{i+1}]</sup>")

    markdown_buffer.write("\n\n")
# Add a Break
markdown_buffer.write('\n----\n')
# And print the footnotes.
markdown_buffer.write("Citations:\n\n")
for i, chunk in enumerate(chunks, start=1):
    markdown_buffer.write(f"{i}. [{chunk.web.title}]({chunk.web.uri})\n")
# Add a Break
markdown_buffer.write('\n----\n')

# Display all the markdown
Markdown(markdown_buffer.getvalue())