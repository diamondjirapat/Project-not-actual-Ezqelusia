import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://admin:secure_password@localhost:5432/1000000_bandcamp_sales')
query = 'SELECT * FROM raw_data'

df = pd.read_sql(query, engine)

print(df.head())

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Cleaning
df.drop(
[
    "utc_date", "track_album_slug_text", "item_type", "amount_paid_fmt", "art_id", "amount_paid", "releases",
    "currency", "package_image_id", "amount_over_fmt", "item_slug", "addl_count", "_id", "country_code",
    "url", "art_url", "item_price"
],
    axis=1, inplace=True
)

df.dropna(inplace=True)
df.drop(df[df['slug_type'] == 'p'].index, inplace=True)


# Transformation
df['id'] = range(1, len(df) + 1)

cols = ['id'] + [col for col in df.columns if col != 'id']
df = df[cols]


df['slug_type'] = df['slug_type'].replace('a', 'album')
df['slug_type'] = df['slug_type'].replace('t', 'track')

# Aggregation
total_sales = df['amount_paid_usd'].sum()
top_5_countries = df.groupby('country')['amount_paid_usd'].sum().nlargest(5)
top_5_df = top_5_countries.to_frame(name='revenue')
top_5_df['percentage'] = (top_5_df['revenue'] / total_sales) * 100
top_5_df['percentage'] = top_5_df['percentage'].round(2)

print(f"Total Sales: ${total_sales:,.2f}")
print("-" * 30)
print(top_5_df)

top_songs = df[df['slug_type'] == 'track'].groupby('item_description')['amount_paid_usd'].sum().nlargest(10)
print(f"\n2. Top 10 Songs:\n{top_songs}")

top_albums = df.groupby('album_title')['amount_paid_usd'].sum().nlargest(10)
print(f"\n3. Top 10 Albums:\n{top_albums}")

top_artists = df.groupby('artist_name')['amount_paid_usd'].sum().nlargest(5)
print(f"\n4. Top 5 Artists:\n{top_artists}")

revenue_share = df.groupby('slug_type')['amount_paid_usd'].sum().sort_values(ascending=False)
revenue_share_pct = (revenue_share / revenue_share.sum()) * 100
print(f"\n5. Revenue Share by Type (%):\n{revenue_share_pct}")


print("\n Saving to Database...")
try:
    df.to_sql(
        name='production',
        con=engine,
        if_exists='append',
        index=False
    )
    print(f"\n successful")

except Exception as e:
    print(f"Error: {e}")
