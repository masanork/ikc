異体字漢字コンバーターの作成方法
===

## main.rsの作成

### Prompt

Rustで異体字を正字に変換するフィルターを作成してください。標準入力で受け取ったテキストデータについて、異体字を正字に変換したテキストを標準出力に出力してください。ソースコードと同じディレクトリにある itaiji.csv には正字、異体字の順で対応表が記載されています。この対応表はUTF-8で記述されています。include_str!マクロを使用してファイルの内容をソースコード中の文字列リテラルとして直接埋め込んでください。-hまたは--helpオプションを指定した場合は、異体字漢字コンバーターの使用方法を表示してください。-vまたは--versionオプションを指定した場合は、異体字漢字コンバーターのバージョン情報を表示してください。-iまたは--inputオプションを指定した場合は、標準入力ではなく、指定したファイルを入力ファイルとして扱ってください。-oまたは--outputオプションを指定した場合は、標準出力ではなく、指定したファイルを出力ファイルとして扱ってください。

### Anser

以下は、Rustで指定された要件に基づいて異体字を正字に変換するフィルターのプログラムです。

```rust
use std::fs::File;
use std::io::{self, BufRead, BufReader, Write};
use std::collections::HashMap;
use structopt::StructOpt;

const ITAIJI: &str = include_str!("itaiji.csv");

#[derive(StructOpt, Debug)]
struct Opt {
    #[structopt(short = "i", long = "input")]
    input_file: Option<String>,
    #[structopt(short = "o", long = "output")]
    output_file: Option<String>,
    #[structopt(short = "h", long = "help")]
    help: bool,
    #[structopt(short = "v", long = "version")]
    version: bool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let opt = Opt::from_args();

    if opt.help {
        println!("異体字漢字コンバーターの使用方法:\nオプション:
                -i, --input <FILE>: 入力ファイルを指定
                -o, --output <FILE>: 出力ファイルを指定
                -h, --help: 使用方法を表示
                -v, --version: バージョン情報を表示");
        return Ok(());
    }

    if opt.version {
        println!("異体字漢字コンバーター バージョン 1.0.0");
        return Ok(());
    }

    let itaiji_map = ITAIJI
        .lines()
        .filter_map(|line| {
            let parts: Vec<&str> = line.split(",").collect();
            if parts.len() == 2 {
                Some((parts[1].to_string(), parts[0].to_string()))
            } else {
                None
            }
        })
        .collect::<HashMap<_, _>>();

    let reader: Box<dyn BufRead> = match opt.input_file {
        Some(input_file) => Box::new(BufReader::new(File::open(input_file)?)),
        None => Box::new(BufReader::new(io::stdin())),
    };

    let mut writer: Box<dyn Write> = match opt.output_file {
        Some(output_file) => Box::new(File::create(output_file)?),
        None => Box::new(io::stdout()),
    };

    for line in reader.lines() {
        let line = line?;
        let converted = line
            .chars()
            .map(|ch| itaiji_map.get(&ch.to_string()).unwrap_or(&ch.to_string()).clone())
            .collect::<String>();
        writeln!(writer, "{}", converted)?;
    }

    Ok(())
}
```

このプログラムは、指定されたオプションを処理し、`itaiji.csv`ファイルから異体字と正字の対応表を読み取り、入力されたテキストデータから異体字を正字に変換します。

必要な外部クレートがあるため、`Cargo.toml`ファイルに以下を追加してください。

```toml
[dependencies]
structopt = "0.3.21"
```

コンバーターを使用するには、コマンドラインから必要なオプションとともに実行してください。

## itaiji.csvの作成

