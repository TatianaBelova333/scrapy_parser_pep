from itertools import chain

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from sqlalchemy import create_engine, func, select, union_all, column
from sqlalchemy.orm import Session

from pep_parse.models import Base, Pep, Status
from pep_parse.settings import BASE_DIR, RESULTS_FOLDER, STATUS_SUMMARY_COLS
from pep_parse.utils import csv_file_output


class PepParsePipeline:

    def open_spider(self, spider):
        """Create db tables and start a db session."""
        engine = create_engine('sqlite:///sqlite.db')
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        """Process an item and record data into database."""
        adapter = ItemAdapter(item)

        item_status = adapter.get('status')
        item_pep_number = adapter.get('number')
        item_pep_name = adapter.get('name')

        if all((item_status, item_pep_number, item_pep_name)):
            db_status = self.session.query(Status).filter(
                Status.status == item_status
            ).one_or_none()

            if not db_status:
                self.session.add(Status(status=item_status))
                self.session.commit()
                db_status = self.session.query(Status).filter(
                    Status.status == item_status
                ).first()

            pep = self.session.query(Pep).filter(
                Pep.pep_number == item_pep_number,
            ).one_or_none()
            if not pep:
                self.session.add(
                    Pep(
                        pep_number=item_pep_number,
                        title=item_pep_name,
                        status_id=db_status.id,
                    )
                )
            self.session.commit()
        else:
            raise DropItem(f"Missing fields in {item}")

        return item

    def status_summary(self):
        """
        Extract data from database and calculate the number of PEP document
        for each status and the total number of all PEP docs.

        """
        file_prefix = self.status_summary.__name__
        status_summary_cols = STATUS_SUMMARY_COLS

        pep_stat_num_qry = select(
            Status.status, func.count(Pep.status_id)
        ).join(
            Pep, Pep.status_id == Status.id,
        ).group_by(Pep.status_id)

        peps_total_qry = select(column('TOTAL'), func.count(Pep.id))

        db_query = self.session.execute(
            union_all(pep_stat_num_qry, peps_total_qry),
        )

        summary_results = chain(
            (status_summary_cols,),
            db_query,
        )

        csv_file_output(
            base_dir=BASE_DIR,
            dir_name=RESULTS_FOLDER,
            file_prefix=file_prefix,
            data=summary_results
        )

    def close_spider(self, spider):
        self.status_summary()
        self.session.close()
