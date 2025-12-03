-- Create ENUM type for content type
CREATE TYPE content_type_enum AS ENUM ('text', 'image');

-- Create items table
CREATE TABLE IF NOT EXISTS items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    short_code VARCHAR(10) UNIQUE NOT NULL,
    type content_type_enum NOT NULL,
    original_content TEXT,
    file_path TEXT,
    original_size_kb INTEGER NOT NULL CHECK (original_size_kb >= 0),
    compressed_size_kb INTEGER NOT NULL CHECK (compressed_size_kb >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT check_content_or_file CHECK (
        (type = 'text' AND original_content IS NOT NULL AND file_path IS NULL) OR
        (type = 'image' AND original_content IS NULL AND file_path IS NOT NULL)
    )
);

-- Create indexes
CREATE INDEX idx_short_code ON items(short_code);
CREATE INDEX idx_created_at ON items(created_at);
CREATE INDEX idx_expires_at ON items(expires_at) WHERE expires_at IS NOT NULL;

-- Enable Row Level Security (RLS)
ALTER TABLE items ENABLE ROW LEVEL SECURITY;

-- Create policy for public read access
CREATE POLICY "Enable read access for all users" ON items
    FOR SELECT USING (true);

-- Create policy for authenticated insert (or allow all for MVP)
CREATE POLICY "Enable insert for all users" ON items
    FOR INSERT WITH CHECK (true);

-- Create policy for deleting expired items
CREATE POLICY "Enable delete for expired items" ON items
    FOR DELETE USING (expires_at IS NULL OR expires_at > NOW());
