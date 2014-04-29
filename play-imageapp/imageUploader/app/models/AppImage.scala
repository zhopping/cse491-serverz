package models
import play.api.db._
import play.api.Play.current
import anorm._
import anorm.SqlParser._
case class AppImage(id: Long, data: Array[Byte])

import play.api._
object AppImage {
	val img = {
		get[Long]("images.Id") ~ 
		get[Array[Byte]]("images.Data") map {
			case id~data => AppImage(id, data)
		}
	}
	implicit def rowToByteArray: Column[Array[Byte]] = Column.nonNull { (value, meta) =>
		val MetaDataItem(qualified, nullable, clazz) = meta
		value match 
		{
		case data: Array[Byte] => Right(data)
		case _ => Left(TypeDoesNotMatch("Cannot convert " + value + ":" + value.asInstanceOf[AnyRef].getClass + " to Byte Array for column " + qualified))
		}
	}
	def bytes(columnName: String): RowParser[Array[Byte]] = get[Array[Byte]](columnName)(implicitly[Column[Array[Byte]]])

	def get_latest_image : AppImage = DB.withConnection { implicit c =>
		SQL("select * from images order by id desc limit 1").as(img.single)
	}

	def get_count : Long = DB.withConnection { implicit c =>
		SQL("Select count(*) as c from images").apply().head[Long]("c")
	}

	def add(mdata: Array[Byte]){ 
		DB.withConnection { implicit c =>
		SQL(
			"""
			INSERT INTO images 
			(Data, DTSInserted) 
			VALUES ({data},DateTime('now'))
			"""
			).on("data" -> mdata).executeUpdate()
		}
		Logger.info(mdata.toString());
	}

	def delete(id: Long) {}
  
}